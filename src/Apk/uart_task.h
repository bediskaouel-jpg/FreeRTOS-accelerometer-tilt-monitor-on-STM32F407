/*
 * uart_task.h
 *
 */

#include <stdint.h>

#ifndef APK_UART_TASK_H_
#define APK_UART_TASK_H_

#define CMD_SEND_XY_VAL 0xA1
#define CMD_RESET_XY_THR 0xB1
#define CMD_UPDATE_XY_THR 0xFF
#define SOF_PATTERN 0xAA

typedef struct
{
	uint32_t DATA;
	uint16_t CONFIG;
	uint8_t SOF;
	uint8_t CMD;
}FrameUART;

typedef enum
{
	WAIT_FOR_SOF,
	WAIT_FOR_CMD,
	WAIT_FOR_CONFIG,
	WAIT_FOR_DATA
}StateFrame;

uint8_t UART_Init(void);
void UARTTask(void * pvParameters);
void SendFrame(const FrameUART *Frame);
void SendAccelero(int16_t X_mg, int16_t Y_mg);

#endif /* APK_UART_TASK_H_ */
