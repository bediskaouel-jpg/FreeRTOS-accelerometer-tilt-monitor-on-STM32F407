#!/usr/bin/env python3
"""
STM32F407 Accelerometer Dashboard
=================================
A production-quality PyQt5 application for communicating with an STM32F407 microcontroller
over UART. Receives 2D accelerometer data, visualizes movement with smooth rendering,
manages threshold levels, controls directional LEDs, and monitors communication metrics.

Architecture:
  - FrameUART: Data structure for 8-byte binary frame packing/unpacking.
  - SerialThread: Dedicated QThread for non-blocking UART I/O, parsing, and buffer recovery.
  - MovementWidget: Custom QWidget for real-time visual tracking of STM32 orientation & thresholds.
  - LCDDisplay: Styled Qt widget providing digital-counter style dynamic readouts.
  - MainWindow: Master UI container integrating top bar, side controls, viz center, & status bar.

Author: Kaouel Badis
License: MIT
"""

import math
import struct
import sys
import time
from typing import List, Optional, Tuple

import serial
import serial.tools.list_ports
from PyQt5.QtCore import QPointF, QRectF, QSize, Qt, QThread, QTimer, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QFont, QIcon, QPainter, QPen, QPainterPath
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


# ==============================================================================
# PROTOCOL DEFINITIONS & FRAME PARSING
# ==============================================================================

class FrameUART:
    """
    Encapsulates the 8-byte UART communication frame binary layout.
    
    Binary Structure (Little-Endian):
      Byte 0: SOF (Start of Frame) - Always 0xAA
      Byte 1: CMD (Command Code)
      Byte 2: CONFIG LSB - Always 0x00
      Byte 3: CONFIG MSB - Always 0x00
      Byte 4: DATA Byte 0 (LSB)
      Byte 5: DATA Byte 1
      Byte 6: DATA Byte 2
      Byte 7: DATA Byte 3 (MSB)
    """

    SOF_VAL: int = 0xAA
    CONFIG_VAL: int = 0x0000
    FRAME_SIZE: int = 8

    # Command Definitions
    CMD_ACCEL_DATA: int = 0xA1
    CMD_RESET: int = 0xB1
    CMD_THRESHOLD_UPDATE: int = 0xFF
    CMD_LED_LEFT: int = 0xC1
    CMD_LED_RIGHT: int = 0xD1
    CMD_LED_UP: int = 0xE1
    CMD_LED_DOWN: int = 0xF1

    # Commands the STM32 can send: used to validate the start of a frame
    RX_COMMANDS: Tuple[int, ...] = (CMD_ACCEL_DATA, CMD_RESET)

    # Struct format: < (Little-Endian), B (SOF), B (CMD), H (CONFIG), I (DATA)
    STRUCT_FORMAT: str = "<BBHI"

    def __init__(self, cmd: int = 0x00, data: int = 0, config: int = CONFIG_VAL, sof: int = SOF_VAL):
        self.sof: int = sof
        self.cmd: int = cmd
        self.config: int = config
        self.data: int = data

    def pack(self) -> bytes:
        """Packs the internal fields into an 8-byte binary string."""
        return struct.pack(self.STRUCT_FORMAT, self.sof, self.cmd, self.config, self.data & 0xFFFFFFFF)

    @classmethod
    def unpack(cls, raw_bytes: bytes) -> "FrameUART":
        """Unpacks 8 bytes into a FrameUART object."""
        if len(raw_bytes) != cls.FRAME_SIZE:
            raise ValueError(f"Expected frame length {cls.FRAME_SIZE}, got {len(raw_bytes)}")
        sof, cmd, config, data = struct.unpack(cls.STRUCT_FORMAT, raw_bytes)
        return cls(cmd=cmd, data=data, config=config, sof=sof)

    @staticmethod
    def encode_thresholds(x_thresh: int, y_thresh: int) -> int:
        """
        Encodes signed 16-bit X and Y thresholds into a single 32-bit uint DATA word.
        Bits 31..16 = Y Threshold
        Bits 15..0  = X Threshold
        """
        x_16 = x_thresh & 0xFFFF
        y_16 = y_thresh & 0xFFFF
        return (y_16 << 16) | x_16

    @staticmethod
    def decode_accel_data(data_word: int) -> Tuple[int, int]:
        """
        Decodes a 32-bit DATA word into signed 16-bit X and Y accelerometer values.
        Bits 31..16 = X
        Bits 15..0  = Y
        """
        raw_x = (data_word >> 16) & 0xFFFF
        raw_y = data_word & 0xFFFF
        
        # Convert uint16 to signed int16
        x_val = raw_x - 0x10000 if raw_x >= 0x8000 else raw_x
        y_val = raw_y - 0x10000 if raw_y >= 0x8000 else raw_y
        
        return x_val, y_val


# ==============================================================================
# WORKER THREAD FOR SERIAL COMMUNICATIONS
# ==============================================================================

class SerialThread(QThread):
    """
    Dedicated QThread responsible for async serial I/O, ring buffering, frame 
    synchronization on SOF, and emitting parsed metrics to the GUI.
    """

    frame_received = pyqtSignal(FrameUART)
    accel_data_received = pyqtSignal(int, int)  # X, Y
    reset_command_received = pyqtSignal()
    connection_status_changed = pyqtSignal(bool, str)
    metrics_updated = pyqtSignal(int, int, float)  # rx_count, err_count, fps
    error_occurred = pyqtSignal(str)

    def __init__(self, port: str, baudrate: int = 115200, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.port: str = port
        self.baudrate: int = baudrate
        self._is_running: bool = False
        self._serial: Optional[serial.Serial] = None
        
        # Metrics Tracking
        self.rx_count: int = 0
        self.error_count: int = 0
        self.frame_times: List[float] = []

    def run(self) -> None:
        """Main thread loop handling hardware I/O and stream framing."""
        self._is_running = True
        rx_buffer = bytearray()
        
        try:
            self._serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=0.02
            )
            self.connection_status_changed.emit(True, f"Connected to {self.port}")
        except Exception as e:
            self.connection_status_changed.emit(False, f"Connection Failed: {str(e)}")
            self._is_running = False
            return

        last_fps_calc = time.time()
        fps_frame_count = 0
        current_fps = 0.0

        while self._is_running:
            try:
                if self._serial and self._serial.in_waiting > 0:
                    raw_data = self._serial.read(self._serial.in_waiting)
                    if raw_data:
                        rx_buffer.extend(raw_data)

                # Process buffer for valid 8-byte frames synchronized on SOF (0xAA)
                while len(rx_buffer) >= FrameUART.FRAME_SIZE:
                    # Sync to SOF followed by a known command (0xAA can also appear in the data)
                    if rx_buffer[0] != FrameUART.SOF_VAL or rx_buffer[1] not in FrameUART.RX_COMMANDS:
                        rx_buffer.pop(0)
                        self.error_count += 1
                        continue

                    # Extract candidate frame
                    candidate_frame_bytes = bytes(rx_buffer[:FrameUART.FRAME_SIZE])
                    
                    try:
                        frame = FrameUART.unpack(candidate_frame_bytes)
                        # Remove processed frame bytes from buffer
                        del rx_buffer[:FrameUART.FRAME_SIZE]
                        
                        self.rx_count += 1
                        fps_frame_count += 1
                        
                        # Process frame command payload
                        self._handle_frame(frame)

                    except Exception:
                        # Corrupted payload structure: slide frame window by 1 byte to re-sync
                        rx_buffer.pop(0)
                        self.error_count += 1

                # Calculate metrics once every second
                now = time.time()
                if now - last_fps_calc >= 1.0:
                    current_fps = fps_frame_count / (now - last_fps_calc)
                    fps_frame_count = 0
                    last_fps_calc = now
                    self.metrics_updated.emit(self.rx_count, self.error_count, current_fps)

                self.msleep(5)

            except serial.SerialException as se:
                self.error_occurred.emit(f"Hardware Error: {str(se)}")
                self.connection_status_changed.emit(False, "Connection Lost")
                break
            except Exception as e:
                self.error_occurred.emit(f"Unexpected UART Error: {str(e)}")
                self.error_count += 1

        self._close_serial()

    def _handle_frame(self, frame: FrameUART) -> None:
        """Routes parsed UART frame payloads to specific signals."""
        self.frame_received.emit(frame)
        
        if frame.cmd == FrameUART.CMD_ACCEL_DATA:
            x, y = FrameUART.decode_accel_data(frame.data)
            self.accel_data_received.emit(x, y)
        elif frame.cmd == FrameUART.CMD_RESET:
            self.reset_command_received.emit()

    def send_frame(self, frame: FrameUART) -> bool:
        """Sends a structured FrameUART object to the serial port."""
        if self._serial and self._serial.is_open:
            try:
                data_to_send = frame.pack()
                written = self._serial.write(data_to_send)
                self._serial.flush()
                return written == len(data_to_send)
            except Exception as e:
                self.error_occurred.emit(f"Failed to transmit frame: {str(e)}")
                return False
        return False

    def stop(self) -> None:
        """Signals thread loop termination and waits for execution cleanup."""
        self._is_running = False
        self.wait(1000)

    def _close_serial(self) -> None:
        """Safely disposes of the PySerial device handle."""
        if self._serial:
            try:
                if self._serial.is_open:
                    self._serial.close()
            except Exception:
                pass
            self._serial = None


# ==============================================================================
# CUSTOM VISUALIZATION & LCD WIDGETS
# ==============================================================================

class MovementWidget(QWidget):
    """
    Custom QWidget rendering dynamic accelerometer spatial movement, axis scales,
    threshold boundary rectangles, and high-DPI graphic overlays.
    """

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        # Position Data
        self.current_x: float = 0.0
        self.current_y: float = 0.0
        self.target_x: float = 0.0
        self.target_y: float = 0.0
        
        # Threshold Limits
        self.thresh_x: float = 200.0
        self.thresh_y: float = 200.0
        
        # Maximum expected dynamic range for coordinate projection
        self.max_range: float = 600.0
        
        # Motion Smoothing Timer (60 FPS rendering target)
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self._update_animation)
        self.anim_timer.start(16)

        self.setMinimumSize(450, 450)

    def set_position(self, x: int, y: int) -> None:
        """Sets target positional values for interpolated movement."""
        self.target_x = float(x)
        self.target_y = float(y)

    def set_thresholds(self, thresh_x: int, thresh_y: int) -> None:
        """Updates threshold boundary values and requests redraw."""
        self.thresh_x = max(1.0, float(thresh_x))
        self.thresh_y = max(1.0, float(thresh_y))
        self.update()

    def _update_animation(self) -> None:
        """Smoothly interpolates movement box towards target position."""
        # Exponential smoothing linear interpolation (LERP)
        alpha = 0.25
        diff_x = self.target_x - self.current_x
        diff_y = self.target_y - self.current_y
        
        if abs(diff_x) > 0.01 or abs(diff_y) > 0.01:
            self.current_x += diff_x * alpha
            self.current_y += diff_y * alpha
            self.update()

    def paintEvent(self, event) -> None:
        """Handles custom hardware-accelerated QPainter UI rendering."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        center_x = width / 2.0
        center_y = height / 2.0
        
        # Fill background dark canvas
        painter.fillRect(self.rect(), QColor("#121418"))
        
        # Compute scaling metrics (scale axis dynamically to widget dimensions)
        margin = 40.0
        usable_radius = min(center_x, center_y) - margin
        scale_factor = usable_radius / self.max_range

        # 1. Draw Grid Lines and Polar Rings
        grid_pen = QPen(QColor("#2A2E3D"), 1, Qt.DashLine)
        painter.setPen(grid_pen)
        
        for r_step in [100, 200, 300, 400, 500, 600]:
            r_pix = r_step * scale_factor
            painter.drawEllipse(QPointF(center_x, center_y), r_pix, r_pix)

        # 2. Draw Center Coordinates Axes
        axis_pen = QPen(QColor("#4A5168"), 2)
        painter.setPen(axis_pen)
        painter.drawLine(QPointF(margin, center_y), QPointF(width - margin, center_y))
        painter.drawLine(QPointF(center_x, margin), QPointF(center_x, height - margin))

        # 3. Draw Axis Labels
        font_axis = QFont("Segoe UI", 9, QFont.Bold)
        painter.setFont(font_axis)
        painter.setPen(QPen(QColor("#7A829E")))
        painter.drawText(int(width - margin + 8), int(center_y + 4), "+X")
        painter.drawText(int(margin - 25), int(center_y + 4), "-X")
        painter.drawText(int(center_x - 8), int(margin - 10), "+Y")
        painter.drawText(int(center_x - 8), int(height - margin + 20), "-Y")

        # 4. Draw Threshold Rectangles
        rect_w = self.thresh_x * scale_factor * 2.0
        rect_h = self.thresh_y * scale_factor * 2.0
        thresh_rect = QRectF(center_x - rect_w / 2.0, center_y - rect_h / 2.0, rect_w, rect_h)
        
        # Clamp threshold rect bounding inside canvas view
        thresh_pen = QPen(QColor("#FF9800"), 2, Qt.DashLine)
        painter.setPen(thresh_pen)
        painter.setBrush(QBrush(QColor(255, 152, 0, 15)))  # Soft orange translucent highlight
        painter.drawRect(thresh_rect)

        # Draw threshold scalar readout labels adjacent to bounding rect
        painter.setFont(QFont("Segoe UI", 9, QFont.Bold))
        painter.setPen(QPen(QColor("#FFB74D")))
        painter.drawText(int(thresh_rect.right() + 6), int(thresh_rect.top() - 6), f"Tx: {int(self.thresh_x)}")
        painter.drawText(int(thresh_rect.left() - 65), int(thresh_rect.bottom() + 15), f"Ty: {int(self.thresh_y)}")

        # 5. Draw Target Track Indicator Point/Square
        # Mapping physical coords to GUI Canvas: Screen Y axis is inverted relative to Cartesian Y
        px = center_x + (self.current_x * scale_factor)
        py = center_y - (self.current_y * scale_factor)

        # Clamp position coordinates within widget bounds with safety margins
        sq_size = 70.0
        px = max(sq_size / 2.0 + 5, min(width - sq_size / 2.0 - 5, px))
        py = max(sq_size / 2.0 + 5, min(height - sq_size / 2.0 - 5, py))

        box_rect = QRectF(px - sq_size / 2.0, py - sq_size / 2.0, sq_size, sq_size)

        # Determine if inside safe stable region
        is_stable = abs(self.current_x) <= self.thresh_x and abs(self.current_y) <= self.thresh_y
        
        box_border_color = QColor("#00E676") if is_stable else QColor("#FF1744")
        box_fill_color = QColor(13, 71, 161, 210)  # Modern deep blue box highlight

        painter.setPen(QPen(box_border_color, 2))
        painter.setBrush(QBrush(box_fill_color))
        painter.drawRoundedRect(box_rect, 8.0, 8.0)

        # Text label inside movement target square
        painter.setFont(QFont("Segoe UI", 10, QFont.Bold))
        painter.setPen(QPen(QColor("#FFFFFF")))
        painter.drawText(box_rect, Qt.AlignCenter, "STM32F4")

        # Draw connecting line from origin (0,0) to object box center
        line_pen = QPen(QColor(33, 150, 243, 160), 1.5, Qt.DotLine)
        painter.setPen(line_pen)
        painter.drawLine(QPointF(center_x, center_y), QPointF(px, py))


class LCDDisplayWidget(QFrame):
    """Modern dark themed segmented numeric indicator display."""

    def __init__(self, title: str, initial_value: str = "0", unit: str = "", parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            LCDDisplayWidget {
                background-color: #1A1D24;
                border: 1px solid #2C3240;
                border-radius: 6px;
                padding: 6px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(2)

        self.title_label = QLabel(title.upper())
        self.title_label.setStyleSheet("color: #7A829E; font-size: 10px; font-weight: bold; letter-spacing: 1px;")

        self.value_label = QLabel(initial_value)
        self.value_label.setFont(QFont("Consolas", 22, QFont.Bold))
        self.value_label.setStyleSheet("color: #00E676; background-color: #0D1117; border-radius: 4px; padding: 4px 8px;")
        self.value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)

    def set_value(self, val: str) -> None:
        """Updates display text smoothly."""
        self.value_label.setText(val)

    def set_accent_color(self, hex_color: str) -> None:
        """Updates text display CSS theme color dynamically."""
        self.value_label.setStyleSheet(f"color: {hex_color}; background-color: #0D1117; border-radius: 4px; padding: 4px 8px;")


# ==============================================================================
# MAIN APPLICATION WINDOW
# ==============================================================================

class MainWindow(QMainWindow):

    DEFAULT_THRESHOLD: int = 200

    """
    Main application window implementing custom controls, panel layouts,
    signals/slots connection routing, and error dialog handling.
    """

    def __init__(self):
        super().__init__()

        # State Variables
        self.serial_thread: Optional[SerialThread] = None
        self.current_thresh_x: int = 200
        self.current_thresh_y: int = 200
        self.led_states = {"LEFT": True, "RIGHT": True, "UP": True, "DOWN": True}

        # Configure GUI Surface Properties
        self.setWindowTitle("STM32F407 Accelerometer Dashboard")
        self.setMinimumSize(1400, 850)
        self.setFont(QFont("Segoe UI", 10))

        # Build Main View Hierarchy
        self._apply_global_theme()
        self._init_ui()

        # Connect Port Refresh Auto Detector
        self._refresh_com_ports()

    # --------------------------------------------------------------------------
    # GLOBAL STYLESHEET
    # --------------------------------------------------------------------------
    def _apply_global_theme(self) -> None:
        """Sets dark theme stylesheet styling for all child QWidgets."""
        dark_theme = """
            QMainWindow {
                background-color: #0F1115;
            }
            QWidget {
                color: #E0E6ED;
                font-family: 'Segoe UI', sans-serif;
            }
            QGroupBox {
                background-color: #161920;
                border: 1px solid #262C3A;
                border-radius: 8px;
                margin-top: 12px;
                font-weight: bold;
                font-size: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 2px 8px;
                color: #00E676;
            }
            QPushButton {
                background-color: #212631;
                border: 1px solid #323A4C;
                border-radius: 5px;
                color: #FFFFFF;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2B3242;
                border-color: #434D66;
            }
            QPushButton:pressed {
                background-color: #181C24;
            }
            QPushButton:disabled {
                background-color: #12141A;
                color: #485066;
                border-color: #1C202B;
            }
            QLineEdit {
                background-color: #0D0F12;
                border: 1px solid #2A303D;
                border-radius: 4px;
                color: #00E676;
                padding: 6px;
                font-family: 'Consolas', monospace;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #00E676;
            }
            QComboBox {
                background-color: #1A1D24;
                border: 1px solid #2C3240;
                border-radius: 4px;
                padding: 6px;
                min-width: 140px;
            }
            QComboBox::drop-down {
                border: 0px;
            }
            QTableWidget {
                background-color: #12141A;
                border: 1px solid #222733;
                gridline-color: #1F2430;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #1A1D25;
                color: #8A92A6;
                padding: 4px;
                border: none;
                font-weight: bold;
            }
        """
        self.setStyleSheet(dark_theme)

    # --------------------------------------------------------------------------
    # UI SETUP INITIALIZATION
    # --------------------------------------------------------------------------
    def _init_ui(self) -> None:
        """Instantiates all UI layouts, widgets, panels, and sidebars."""
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_vbox = QVBoxLayout(central_widget)
        main_vbox.setContentsMargins(12, 12, 12, 12)
        main_vbox.setSpacing(10)

        # Build Integrated Top Connection Bar
        top_bar = self._create_top_bar()
        main_vbox.addLayout(top_bar)

        # Build Main Body Splitter Layout (Left, Center, Right)
        body_splitter = QSplitter(Qt.Horizontal)
        body_splitter.setChildrenCollapsible(False)

        # 1. Left Control Panel
        left_panel = self._create_left_panel()
        body_splitter.addWidget(left_panel)

        # 2. Center Visualization Canvas
        center_panel = self._create_center_panel()
        body_splitter.addWidget(center_panel)

        # 3. Right Telemetry Panel
        right_panel = self._create_right_panel()
        body_splitter.addWidget(right_panel)

        # Adjust panel default split ratios (Left: 22%, Center: 56%, Right: 22%)
        body_splitter.setSizes([300, 750, 350])
        main_vbox.addWidget(body_splitter, stretch=1)

        # Build Bottom Status Bar
        status_bar_layout = self._create_status_bar()
        main_vbox.addLayout(status_bar_layout)

    # --------------------------------------------------------------------------
    # TOP CONNECTION BAR
    # --------------------------------------------------------------------------
    def _create_top_bar(self) -> QHBoxLayout:
        """Constructs the device COM connectivity bar."""
        layout = QHBoxLayout()
        layout.setSpacing(10)

        bar_frame = QFrame()
        bar_frame.setStyleSheet("background-color: #161920; border: 1px solid #262C3A; border-radius: 6px;")
        frame_layout = QHBoxLayout(bar_frame)
        frame_layout.setContentsMargins(12, 8, 12, 8)

        # COM Port Selector Labels & Box
        lbl_port = QLabel("Serial Port:")
        lbl_port.setStyleSheet("border: none; font-weight: bold;")
        self.combo_ports = QComboBox()

        self.btn_refresh = QPushButton("Refresh Ports")
        self.btn_refresh.clicked.connect(self._refresh_com_ports)

        self.btn_connect = QPushButton("Connect")
        self.btn_connect.setStyleSheet("""
            QPushButton { background-color: #2E7D32; border-color: #388E3C; }
            QPushButton:hover { background-color: #388E3C; }
        """)
        self.btn_connect.clicked.connect(self._connect_serial)

        self.btn_disconnect = QPushButton("Disconnect")
        self.btn_disconnect.setEnabled(False)
        self.btn_disconnect.setStyleSheet("""
            QPushButton { background-color: #C62828; border-color: #D32F2F; }
            QPushButton:hover { background-color: #D32F2F; }
        """)
        self.btn_disconnect.clicked.connect(self._disconnect_serial)

        # Connection Indicator Icon & Label
        self.lbl_status_icon = QLabel("●")
        self.lbl_status_icon.setStyleSheet("color: #FF1744; font-size: 18px; border: none;")
        self.lbl_status_text = QLabel("Not Connected")
        self.lbl_status_text.setStyleSheet("font-weight: bold; color: #8A92A6; border: none;")

        frame_layout.addWidget(lbl_port)
        frame_layout.addWidget(self.combo_ports)
        frame_layout.addWidget(self.btn_refresh)
        frame_layout.addWidget(self.btn_connect)
        frame_layout.addWidget(self.btn_disconnect)
        frame_layout.addSpacing(20)
        frame_layout.addWidget(self.lbl_status_icon)
        frame_layout.addWidget(self.lbl_status_text)
        frame_layout.addStretch()

        layout.addWidget(bar_frame)
        return layout

    # --------------------------------------------------------------------------
    # LEFT PANEL: CONTROLS & THRESHOLDS
    # --------------------------------------------------------------------------
    def _create_left_panel(self) -> QWidget:
        """Constructs Left Side control GroupBoxes."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # --- GroupBox 1: LED Direction Controls ---
        grp_led = QGroupBox("LED CONTROLS")
        led_grid = QGridLayout(grp_led)
        led_grid.setContentsMargins(12, 16, 12, 12)
        led_grid.setSpacing(10)

        self.btn_led_up = self._create_toggle_button("Up LED", True)
        self.btn_led_down = self._create_toggle_button("Down LED", True)
        self.btn_led_left = self._create_toggle_button("Left LED", True)
        self.btn_led_right = self._create_toggle_button("Right LED", True)

        # Cross arrangement for LEDs
        led_grid.addWidget(self.btn_led_up, 0, 1)
        led_grid.addWidget(self.btn_led_left, 1, 0)
        led_grid.addWidget(self.btn_led_right, 1, 2)
        led_grid.addWidget(self.btn_led_down, 2, 1)

        self.btn_led_left.clicked.connect(lambda: self._toggle_led("LEFT", FrameUART.CMD_LED_LEFT, self.btn_led_left))
        self.btn_led_right.clicked.connect(lambda: self._toggle_led("RIGHT", FrameUART.CMD_LED_RIGHT, self.btn_led_right))
        self.btn_led_up.clicked.connect(lambda: self._toggle_led("UP", FrameUART.CMD_LED_UP, self.btn_led_up))
        self.btn_led_down.clicked.connect(lambda: self._toggle_led("DOWN", FrameUART.CMD_LED_DOWN, self.btn_led_down))

        # --- GroupBox 2: Threshold Configurations ---
        grp_thresh = QGroupBox("THRESHOLD CONFIGURATION")
        thresh_layout = QVBoxLayout(grp_thresh)
        thresh_layout.setContentsMargins(12, 16, 12, 12)
        thresh_layout.setSpacing(10)

        # Read-Only Active Registers Displays
        lbl_curr_x_title = QLabel("Current Active X Threshold:")
        self.lbl_curr_thresh_x = QLabel("200")
        self.lbl_curr_thresh_x.setStyleSheet("font-family: Consolas; font-size: 14px; color: #00E676; font-weight: bold;")

        lbl_curr_y_title = QLabel("Current Active Y Threshold:")
        self.lbl_curr_thresh_y = QLabel("200")
        self.lbl_curr_thresh_y.setStyleSheet("font-family: Consolas; font-size: 14px; color: #00E676; font-weight: bold;")

        # Editable Input Threshold Fields
        lbl_edit_x = QLabel("New Editable X Threshold:")
        self.input_thresh_x = QLineEdit("200")

        lbl_edit_y = QLabel("New Editable Y Threshold:")
        self.input_thresh_y = QLineEdit("200")

        self.btn_send_thresh = QPushButton("Send Thresholds")
        self.btn_send_thresh.setStyleSheet("""
            QPushButton { background-color: #1565C0; border-color: #1E88E5; }
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.btn_send_thresh.clicked.connect(self._send_threshold_command)

        thresh_layout.addWidget(lbl_curr_x_title)
        thresh_layout.addWidget(self.lbl_curr_thresh_x)
        thresh_layout.addWidget(lbl_curr_y_title)
        thresh_layout.addWidget(self.lbl_curr_thresh_y)
        thresh_layout.addSpacing(6)
        thresh_layout.addWidget(lbl_edit_x)
        thresh_layout.addWidget(self.input_thresh_x)
        thresh_layout.addWidget(lbl_edit_y)
        thresh_layout.addWidget(self.input_thresh_y)
        thresh_layout.addSpacing(10)
        thresh_layout.addWidget(self.btn_send_thresh)

        layout.addWidget(grp_led)
        layout.addWidget(grp_thresh)
        layout.addStretch()

        return panel

    def _create_toggle_button(self, text: str, initial_state: bool) -> QPushButton:
        """Helper creating custom directional LED visual toggle buttons."""
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setChecked(initial_state)
        self._update_button_style(btn, initial_state)
        return btn

    def _update_button_style(self, btn: QPushButton, state: bool) -> None:
        """Applies distinct Green (ON) or Gray (OFF) stylesheet state formatting."""
        if state:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2E7D32;
                    color: #FFFFFF;
                    border: 1px solid #4CAF50;
                    border-radius: 6px;
                    padding: 10px;
                    font-weight: bold;
                }
            """)
        else:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #37474F;
                    color: #90A4AE;
                    border: 1px solid #455A64;
                    border-radius: 6px;
                    padding: 10px;
                    font-weight: bold;
                }
            """)

    # --------------------------------------------------------------------------
    # CENTER PANEL: VISUALIZATION CANVAS
    # --------------------------------------------------------------------------
    def _create_center_panel(self) -> QWidget:
        """Constructs central custom motion tracking canvas container."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)

        grp_viz = QGroupBox("SPATIAL MOVEMENT VISUALIZATION")
        viz_layout = QVBoxLayout(grp_viz)
        viz_layout.setContentsMargins(8, 16, 8, 8)

        self.movement_widget = MovementWidget()
        viz_layout.addWidget(self.movement_widget, stretch=1)

        layout.addWidget(grp_viz)
        return panel

    # --------------------------------------------------------------------------
    # RIGHT PANEL: TELEMETRY READOUTS
    # --------------------------------------------------------------------------
    def _create_right_panel(self) -> QWidget:
        """Constructs Right Telemetry and Command History Readout Panel."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # LCD Displays GroupBox
        grp_telemetry = QGroupBox("REAL-TIME TELEMETRY")
        tel_layout = QVBoxLayout(grp_telemetry)
        tel_layout.setContentsMargins(10, 16, 10, 10)
        tel_layout.setSpacing(8)

        self.lcd_x = LCDDisplayWidget("Current X Axis", "0")
        self.lcd_y = LCDDisplayWidget("Current Y Axis", "0")
        self.lcd_thresh_x = LCDDisplayWidget("Threshold X Limit", "200")
        self.lcd_thresh_y = LCDDisplayWidget("Threshold Y Limit", "200")

        self.lcd_thresh_x.set_accent_color("#FFB74D")
        self.lcd_thresh_y.set_accent_color("#FFB74D")

        tel_layout.addWidget(self.lcd_x)
        tel_layout.addWidget(self.lcd_y)
        tel_layout.addWidget(self.lcd_thresh_x)
        tel_layout.addWidget(self.lcd_thresh_y)

        # Communication Metrics Panel
        grp_metrics = QGroupBox("BUS DIAGNOSTICS")
        met_layout = QGridLayout(grp_metrics)
        met_layout.setContentsMargins(10, 16, 10, 10)
        met_layout.setSpacing(6)

        self.lbl_rx_counter = QLabel("0")
        self.lbl_err_counter = QLabel("0")
        self.lbl_fps_rate = QLabel("0.0 Hz")
        self.lbl_last_cmd = QLabel("None (0x00)")

        for lbl in [self.lbl_rx_counter, self.lbl_err_counter, self.lbl_fps_rate, self.lbl_last_cmd]:
            lbl.setStyleSheet("font-family: Consolas; font-weight: bold; color: #64B5F6;")

        met_layout.addWidget(QLabel("Frames Rx:"), 0, 0)
        met_layout.addWidget(self.lbl_rx_counter, 0, 1)
        met_layout.addWidget(QLabel("Bus Errors:"), 1, 0)
        met_layout.addWidget(self.lbl_err_counter, 1, 1)
        met_layout.addWidget(QLabel("UART Rate:"), 2, 0)
        met_layout.addWidget(self.lbl_fps_rate, 2, 1)
        met_layout.addWidget(QLabel("Last Command:"), 3, 0)
        met_layout.addWidget(self.lbl_last_cmd, 3, 1)

        layout.addWidget(grp_telemetry)
        layout.addWidget(grp_metrics)
        layout.addStretch()

        return panel

    # --------------------------------------------------------------------------
    # BOTTOM PANEL: STABILITY STATUS MONITOR
    # --------------------------------------------------------------------------
    def _create_status_bar(self) -> QHBoxLayout:
        """Constructs System Stability Monitor Status Indicator Bar."""
        layout = QHBoxLayout()

        status_frame = QFrame()
        status_frame.setStyleSheet("background-color: #161920; border: 1px solid #262C3A; border-radius: 6px;")
        frame_layout = QHBoxLayout(status_frame)
        frame_layout.setContentsMargins(16, 10, 16, 10)

        lbl_title = QLabel("SYSTEM ACCELEROMETER STATUS:")
        lbl_title.setStyleSheet("font-weight: bold; font-size: 13px; border: none;")

        self.lbl_status_symbol = QLabel("✔")
        self.lbl_status_symbol.setStyleSheet("font-size: 24px; font-weight: bold; color: #00E676; border: none;")

        self.lbl_status_banner = QLabel("STABLE")
        self.lbl_status_banner.setStyleSheet("font-size: 18px; font-weight: bold; color: #00E676; border: none;")

        frame_layout.addWidget(lbl_title)
        frame_layout.addSpacing(15)
        frame_layout.addWidget(self.lbl_status_symbol)
        frame_layout.addWidget(self.lbl_status_banner)
        frame_layout.addStretch()

        layout.addWidget(status_frame)
        return layout

    # --------------------------------------------------------------------------
    # SERIAL CONNECTIONS & LOGIC HANDLERS
    # --------------------------------------------------------------------------
    def _refresh_com_ports(self) -> None:
        """Scans host operating system for available active serial communication ports."""
        self.combo_ports.clear()
        ports = serial.tools.list_ports.comports()
        
        if not ports:
            self.combo_ports.addItem("No COM Ports Found")
            self.btn_connect.setEnabled(False)
            return

        for port_info in ports:
            self.combo_ports.addItem(f"{port_info.device} ({port_info.description})", port_info.device)
        
        self.btn_connect.setEnabled(True)

    def _connect_serial(self) -> None:
        """Instantiates background worker thread to establish hardware serial link."""
        selected_port = self.combo_ports.currentData()
        if not selected_port:
            QMessageBox.critical(self, "Port Error", "Please select a valid COM port from the dropdown.")
            return

        self.serial_thread = SerialThread(port=selected_port, baudrate=115200)
        self.serial_thread.connection_status_changed.connect(self._on_connection_status_changed)
        self.serial_thread.accel_data_received.connect(self._on_accel_data_received)
        self.serial_thread.reset_command_received.connect(self._on_reset_command_received)
        self.serial_thread.frame_received.connect(self._on_frame_received)
        self.serial_thread.metrics_updated.connect(self._on_metrics_updated)
        self.serial_thread.error_occurred.connect(self._on_serial_error)

        self.serial_thread.start()

    def _disconnect_serial(self) -> None:
        """Gracefully releases PySerial connection and worker thread resources."""
        if self.serial_thread:
            self.serial_thread.stop()
            self.serial_thread = None
        self._on_connection_status_changed(False, "Disconnected")

    def _on_connection_status_changed(self, connected: bool, message: str) -> None:
        """Updates UI status indicators based on hardware socket state."""
        if connected:
            self.lbl_status_icon.setStyleSheet("color: #00E676; font-size: 18px; border: none;")
            self.lbl_status_text.setText("Connected")
            self.lbl_status_text.setStyleSheet("font-weight: bold; color: #00E676; border: none;")
            self.btn_connect.setEnabled(False)
            self.btn_disconnect.setEnabled(True)
            self.combo_ports.setEnabled(False)
            self.btn_refresh.setEnabled(False)
        else:
            self.lbl_status_icon.setStyleSheet("color: #FF1744; font-size: 18px; border: none;")
            self.lbl_status_text.setText("Disconnected")
            self.lbl_status_text.setStyleSheet("font-weight: bold; color: #8A92A6; border: none;")
            self.btn_connect.setEnabled(True)
            self.btn_disconnect.setEnabled(False)
            self.combo_ports.setEnabled(True)
            self.btn_refresh.setEnabled(True)

    # --------------------------------------------------------------------------
    # DATA PROCESSORS & UI UPDATERS
    # --------------------------------------------------------------------------
    def _on_accel_data_received(self, x: int, y: int) -> None:
        """Processes CMD 0xA1 positional coordinates."""
        # Update Canvas Position
        self.movement_widget.set_position(x, y)

        # Update LCD Readouts
        self.lcd_x.set_value(str(x))
        self.lcd_y.set_value(str(y))

        # Update System Stability Status
        self._update_system_status(x, y)

    def _update_system_status(self, x: int, y: int) -> None:
        """Evaluates whether current coordinates breach configured stability thresholds."""
        is_stable = (abs(x) <= self.current_thresh_x) and (abs(y) <= self.current_thresh_y)

        if is_stable:
            self.lbl_status_symbol.setText("✔")
            self.lbl_status_symbol.setStyleSheet("font-size: 24px; font-weight: bold; color: #00E676; border: none;")
            self.lbl_status_banner.setText("STABLE")
            self.lbl_status_banner.setStyleSheet("font-size: 18px; font-weight: bold; color: #00E676; border: none;")
        else:
            self.lbl_status_symbol.setText("✖")
            self.lbl_status_symbol.setStyleSheet("font-size: 24px; font-weight: bold; color: #FF1744; border: none;")
            self.lbl_status_banner.setText("TROUBLESHOOT")
            self.lbl_status_banner.setStyleSheet("font-size: 18px; font-weight: bold; color: #FF1744; border: none;")

    def _apply_thresholds(self, tx: int, ty: int) -> None:
        """Met à jour l'état interne et tous les affichages des seuils."""
        self.current_thresh_x = tx
        self.current_thresh_y = ty

        self.lbl_curr_thresh_x.setText(str(tx))
        self.lbl_curr_thresh_y.setText(str(ty))
        self.input_thresh_x.setText(str(tx))
        self.input_thresh_y.setText(str(ty))

        self.lcd_thresh_x.set_value(str(tx))
        self.lcd_thresh_y.set_value(str(ty))

        self.movement_widget.set_thresholds(tx, ty)

    def _on_reset_command_received(self) -> None:
        """Handles reset command CMD 0xB1 from STM32 target."""
        self._apply_thresholds(self.DEFAULT_THRESHOLD, self.DEFAULT_THRESHOLD)

        self.movement_widget.set_position(0, 0)
        self.lcd_x.set_value("0")
        self.lcd_y.set_value("0")
        self._update_system_status(0, 0)

    def _on_frame_received(self, frame: FrameUART) -> None:
        """Logs last command byte received."""
        self.lbl_last_cmd.setText(f"0x{frame.cmd:02X}")

    def _on_metrics_updated(self, rx_count: int, err_count: int, fps: float) -> None:
        """Refreshes diagnostic counter displays."""
        self.lbl_rx_counter.setText(str(rx_count))
        self.lbl_err_counter.setText(str(err_count))
        self.lbl_fps_rate.setText(f"{fps:.1f} Hz")

    def _on_serial_error(self, err_msg: str) -> None:
        """Handles background exceptions safely via popups without crashing UI thread."""
        QMessageBox.warning(self, "Hardware Communication Alert", err_msg)

    # --------------------------------------------------------------------------
    # OUTGOING COMMAND TRANSMITTERS
    # --------------------------------------------------------------------------
    def _toggle_led(self, led_key: str, cmd_code: int, btn: QPushButton) -> None:
        """Packs and dispatches directional LED state frames."""
        new_state = btn.isChecked()
        self.led_states[led_key] = new_state
        self._update_button_style(btn, new_state)

        data_val = 1 if new_state else 0
        frame = FrameUART(cmd=cmd_code, data=data_val)

        if self.serial_thread and self.serial_thread.isRunning():
            self.serial_thread.send_frame(frame)

    def _send_threshold_command(self) -> None:
        """Parses user input boxes and transmits CMD 0xFF threshold frame."""
        try:
            tx_val = int(self.input_thresh_x.text().strip())
            ty_val = int(self.input_thresh_y.text().strip())

            # The STM32 stores the thresholds as unsigned 16-bit values
            if not (0 <= tx_val <= 32767) or not (0 <= ty_val <= 32767):
                raise ValueError("Thresholds must be between 0 and 32767.")

            # Encode thresholds into 32-bit payload
            encoded_data = FrameUART.encode_thresholds(tx_val, ty_val)
            frame = FrameUART(cmd=FrameUART.CMD_THRESHOLD_UPDATE, data=encoded_data)

            if self.serial_thread and self.serial_thread.isRunning():
                if self.serial_thread.send_frame(frame):
                    self._apply_thresholds(tx_val, ty_val)
                else:
                    QMessageBox.warning(self, "Transmission Failed", "Unable to transmit threshold command byte sequence.")
            else:
                QMessageBox.warning(self, "Connection Error", "Please establish a serial link with the STM32 target first.")

        except ValueError as ve:
            QMessageBox.critical(self, "Invalid Input", f"Please enter valid integer thresholds: {str(ve)}")

    def closeEvent(self, event) -> None:
        """Clean resource destruction during window close event."""
        if self.serial_thread:
            self.serial_thread.stop()
        event.accept()


# ==============================================================================
# MAIN EXECUTION ENTRY POINT
# ==============================================================================

def main() -> None:
    """Application main entry point."""
    app = QApplication(sys.argv)
    
    # Configure high DPI desktop scaling support
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()