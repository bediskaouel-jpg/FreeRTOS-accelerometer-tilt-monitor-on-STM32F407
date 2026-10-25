/*
 * uart_task.c
 *
 */

#include "uart_task.h"
#include "sensor_task.h"
#include "led_task.h"
#include "periph_init.h"
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "semphr.h"
#include "stm32f4xx_hal.h"

#define UART_QUEUE_LENGTH   4
#define UART_TX_TIMEOUT_MS  100
#define BUTTON_DEBOUNCE_MS  200

static QueueHandle_t QueueUART = NULL;
static SemaphoreHandle_t TxMutex = NULL;
static uint8_t RxBuffer[10] = {0};
static StateFrame State = WAIT_FOR_SOF;

/*
 * Creates the RX queue and the TX mutex before the scheduler starts,
 * so the UART and button interrupts never see them as NULL.
 * Returns 0 on success.
 */
uint8_t UART_Init(void)
{
	QueueUART = xQueueCreate( UART_QUEUE_LENGTH, sizeof( FrameUART ) );
	TxMutex = xSemaphoreCreateMutex();

	return ((QueueUART == NULL) || (TxMutex == NULL)) ? 1U : 0U;
}

void UARTTask(void * pvParameters)
{
	FrameUART FrameRX = {0};
	(void)pvParameters;

	/* Tell the dashboard that the thresholds are back to their initial values */
	FrameRX.SOF = SOF_PATTERN;
	FrameRX.CMD = CMD_RESET_XY_THR;
	SendFrame(&FrameRX);

	HAL_UART_Receive_IT(&huart2, RxBuffer, 1);

	while(1)
	{
	    xQueueReceive(QueueUART, &FrameRX, portMAX_DELAY );
	    ExecuteCommand(FrameRX);

	    if (FrameRX.CMD == CMD_RESET_XY_THR)
	    {
	        FrameUART Frame = {0};
	        Frame.SOF = SOF_PATTERN;
	        Frame.CMD = CMD_RESET_XY_THR;
	        SendFrame(&Frame);
	    }
	}
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
	static FrameUART   FrameReceived;
	if (huart->Instance == USART2)
	{

		/*Implement FSM*/
		switch (State)
		{
		 case WAIT_FOR_SOF:
		 {  /*Action*/
			 if (RxBuffer[0]== SOF_PATTERN)
			 {
				 FrameReceived.SOF = SOF_PATTERN;
				 State=WAIT_FOR_CMD;
			 }
			 /* otherwise keep waiting for a start of frame */
			 HAL_UART_Receive_IT(&huart2, RxBuffer, 1);
			break;
		 }
		 case WAIT_FOR_CMD:
		 {
			 /*Store Command*/
			 FrameReceived.CMD=RxBuffer[0];
			 HAL_UART_Receive_IT(&huart2, RxBuffer, 2);

			 State=WAIT_FOR_CONFIG;
			break;
		 }
		 case WAIT_FOR_CONFIG:
		 {
			 FrameReceived.CONFIG= ( RxBuffer[0] |(RxBuffer[1]<<8));
			 State=WAIT_FOR_DATA;
			 HAL_UART_Receive_IT(&huart2, RxBuffer, 4);

			 break;
		 }
		 case WAIT_FOR_DATA:
		 {
			 BaseType_t xHigherPriority=pdFALSE;

			 FrameReceived.DATA = (uint32_t)RxBuffer[0] | ((uint32_t)RxBuffer[1]<<8) |
			                      ((uint32_t)RxBuffer[2]<<16) | ((uint32_t)RxBuffer[3]<<24);
			 /*action*/
			 State=WAIT_FOR_SOF;
			 HAL_UART_Receive_IT(&huart2, RxBuffer, 1);

			 /*Notification*/
			 xQueueSendFromISR(QueueUART, &FrameReceived, &xHigherPriority);
			 portYIELD_FROM_ISR(xHigherPriority);

			 break;
		 }
		 default:
		 {
			 State=WAIT_FOR_SOF;
			 HAL_UART_Receive_IT(&huart2, RxBuffer, 1);
			 break;
		 }

		}

	}
}

/*
 * Reception error (overrun, noise, framing). On an overrun the HAL stops
 * the reception for good: restart it and wait for a new frame.
 */
void HAL_UART_ErrorCallback(UART_HandleTypeDef *huart)
{
	if (huart->Instance == USART2)
	{
		HAL_UART_AbortReceive(huart);
		__HAL_UART_CLEAR_OREFLAG(huart);
		State = WAIT_FOR_SOF;
		HAL_UART_Receive_IT(&huart2, RxBuffer, 1);
	}
}

void SendFrame(const FrameUART *Frame)
{
	uint8_t TxBuffer[8];

	TxBuffer[0] = Frame->SOF;
	TxBuffer[1] = Frame->CMD;
	TxBuffer[2] = (uint8_t)(Frame->CONFIG & 0xFF);
	TxBuffer[3] = (uint8_t)((Frame->CONFIG >> 8) & 0xFF);
	TxBuffer[4] = (uint8_t)(Frame->DATA & 0xFF);
	TxBuffer[5] = (uint8_t)((Frame->DATA >> 8) & 0xFF);
	TxBuffer[6] = (uint8_t)((Frame->DATA >> 16) & 0xFF);
	TxBuffer[7] = (uint8_t)((Frame->DATA >> 24) & 0xFF);

	/* Two tasks send frames (sensor and UART): only one at a time on USART2 */
	xSemaphoreTake(TxMutex, portMAX_DELAY);
	HAL_UART_Transmit(&huart2, TxBuffer, sizeof(TxBuffer), UART_TX_TIMEOUT_MS);
	xSemaphoreGive(TxMutex);
}


void SendAccelero(int16_t X_mg, int16_t Y_mg)
{
	FrameUART Frame;
	Frame.SOF = SOF_PATTERN;
	Frame.CMD = CMD_SEND_XY_VAL;
	Frame.CONFIG = 0x0000;
	Frame.DATA = ((uint32_t)(uint16_t)X_mg << 16) | ((uint16_t)Y_mg & 0xFFFF);

	SendFrame(&Frame);
}


/*
 * User button (PA0): asks the UART task to reset the thresholds,
 * exactly as if the command came from the dashboard.
 */
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
	FrameUART Frame = {0};
	BaseType_t xHigherPriority = pdFALSE;
	if ((GPIO_Pin != GPIO_PIN_0) || (QueueUART == NULL))
	{
		return;
	}

	Frame.SOF = SOF_PATTERN;
	Frame.CMD = CMD_RESET_XY_THR;
	xQueueSendFromISR(QueueUART, &Frame, &xHigherPriority);
	portYIELD_FROM_ISR(xHigherPriority);
}

