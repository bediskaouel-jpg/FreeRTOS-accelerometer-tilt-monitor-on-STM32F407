/*
 * led_task.c
 *
 */

#include "led_task.h"
#include "uart_task.h"
#include "sensor_task.h"
#include "main_apk.h"
#include "FreeRTOS.h"
#include "task.h"
#include "stm32f4xx_hal.h"


static uint16_t X_threashhold = X_THREASH_INIT;
static uint16_t Y_threashhold = Y_THREASH_INIT;

static int16_t X_Val = 0;
static int16_t Y_Val = 0;

static int8_t Enable_LED_Left = LED_ON;
static int8_t Enable_LED_right = LED_ON;
static int8_t Enable_LED_down = LED_ON;
static int8_t Enable_LED_up = LED_ON;

void LedTask(void * pvParameters)
{

	SensorData Data = {0};
	TickType_t LastWake = xTaskGetTickCount();
	(void)pvParameters;
	while(1)
	{
		/* Latest sample if a new one arrived, otherwise keep the previous one */
		xQueueReceive(SensorQueue, &Data, 0);
		X_Val = Data.X;
		Y_Val = Data.Y;
		LedUpdate(X_Val, Y_Val);
		vTaskDelayUntil(&LastWake, pdMS_TO_TICKS(LED_PERIOD_MS));
	}

}

void ExecuteCommand(FrameUART Frame)
{
	{
	    uint8_t led_state = (uint8_t)(Frame.DATA & 0x01);

	    switch (Frame.CMD)
	    {
	        case LED_CMD_LEFT:
	            Enable_LED_Left = led_state;
	            break;

	        case LED_CMD_RIGHT:
	            Enable_LED_right = led_state;
	            break;

	        case LED_CMD_UP:
	            Enable_LED_up = led_state;
	            break;

	        case LED_CMD_DOWN:
	            Enable_LED_down = led_state;
	            break;

	        case CMD_UPDATE_XY_THR:
	            X_threashhold = (uint16_t)(Frame.DATA & 0xFFFF);
	            Y_threashhold = (uint16_t)((Frame.DATA >> 16) & 0xFFFF);
	            break;

	        case CMD_RESET_XY_THR:
	        	X_threashhold = X_THREASH_INIT;
	        	Y_threashhold = Y_THREASH_INIT;
	            break;

	        default:
	            break;
	    }
	}
}

void LedUpdate(int16_t X_val, int16_t Y_val)
{
	// LEFT TILT
	if (Enable_LED_Left == LED_ON)
	{
		if(X_val < -X_threashhold)
		{
			HAL_GPIO_TogglePin(GPIOD, GPIO_PIN_12);
		}
		else
		{
			HAL_GPIO_WritePin(GPIOD, GPIO_PIN_12, GPIO_PIN_SET);
		}
	}
	else
	{
		HAL_GPIO_WritePin(GPIOD, GPIO_PIN_12, GPIO_PIN_RESET);
	}
	// RIGHT TILT
	if (Enable_LED_right == LED_ON)
	{
		if(X_val > X_threashhold)
		{
			HAL_GPIO_TogglePin(GPIOD, GPIO_PIN_14);
		}
		else
		{
			HAL_GPIO_WritePin(GPIOD, GPIO_PIN_14, GPIO_PIN_SET);
		}
	}
	else
	{
		HAL_GPIO_WritePin(GPIOD, GPIO_PIN_14, GPIO_PIN_RESET);
	}
	// UP TILT
	if (Enable_LED_up == LED_ON)
	{
		if(Y_val > Y_threashhold)
		{
			HAL_GPIO_TogglePin(GPIOD, GPIO_PIN_13);
		}
		else
		{
			HAL_GPIO_WritePin(GPIOD, GPIO_PIN_13, GPIO_PIN_SET);
		}
	}
	else
	{
		HAL_GPIO_WritePin(GPIOD, GPIO_PIN_13, GPIO_PIN_RESET);
	}
	// DOWN TILT
	if (Enable_LED_down == LED_ON)
	{
		if(Y_val < -Y_threashhold)
		{
			HAL_GPIO_TogglePin(GPIOD, GPIO_PIN_15);
		}
		else
		{
			HAL_GPIO_WritePin(GPIOD, GPIO_PIN_15, GPIO_PIN_SET);
		}
	}
	else
	{
		HAL_GPIO_WritePin(GPIOD, GPIO_PIN_15, GPIO_PIN_RESET);
	}
}

