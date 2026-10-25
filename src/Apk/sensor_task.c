/*
 * sensor_task.c
 *
 */

#include <stdint.h>
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "sensor_task.h"
#include "uart_task.h"
#include "led_task.h"
#include "main_apk.h"
#include "accelero.h"
#include "stm32f4xx_hal.h"

void SensorTask( void * pvParameters )
{
	SensorData Data;
	static int16_t BufferXYZ[3] = {0};
	TickType_t LastWake = xTaskGetTickCount();
	(void)pvParameters;
	while(1)
	{
		acc_getdata(BufferXYZ);
		Data.X = BufferXYZ[0];
		Data.Y = BufferXYZ[1];

		/* Length-1 queue: overwrite, so the LED task always gets the latest sample */
		xQueueOverwrite(SensorQueue, &Data);
		SendAccelero(Data.X, Data.Y);
		vTaskDelayUntil(&LastWake, pdMS_TO_TICKS(SENSOR_PERIOD_MS));
	}

}
