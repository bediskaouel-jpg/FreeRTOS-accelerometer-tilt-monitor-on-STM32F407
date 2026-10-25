/*
 * main_apk.c
 *
 */

#include "main_apk.h"
#include "sensor_task.h"
#include "uart_task.h"
#include "led_task.h"
#include "queue.h"
#include "task.h"
#include "watchdog.h"
#include "global_err.h"


QueueHandle_t    SensorQueue  = NULL;

/*
 * Creates the queues and the tasks. Returns 0 on success.
 */
int MainApk_Init(void)
{
	/* Length 1: the sensor task overwrites the value (xQueueOverwrite)
	 * and the LED task always reads the latest sample */
	SensorQueue = xQueueCreate( 1, sizeof( SensorData ) );
	if ((SensorQueue == NULL) || (UART_Init() != 0))
	{
		return 1;
	}

	if (xTaskCreate(SensorTask, "SENSOR", SENSOR_STACK_SIZE, NULL, SENSOR_PRIORITY, NULL) != pdPASS)
	{
		return 1;
	}

	if (xTaskCreate(LedTask, "LED", LED_STACK_SIZE, NULL, LED_PRIORITY, NULL) != pdPASS)
	{
		return 1;
	}

	if (xTaskCreate(UARTTask, "UART", UART_STACK_SIZE, NULL, UART_PRIORITY, NULL) != pdPASS)
	{
		return 1;
	}

	return 0;
}

/*
 * Called by FreeRTOS when a task overflows its stack
 * (configCHECK_FOR_STACK_OVERFLOW = 2). pcTaskName gives the faulty task.
 */
void vApplicationStackOverflowHook(TaskHandle_t xTask, char *pcTaskName)
{
	(void)xTask;
	(void)pcTaskName;
	vGlobalErrors_globalErrorHandler(DERROR_OVERSTACK_FAIL_);
}

/*
 * Idle task hook (configUSE_IDLE_HOOK = 1): refreshes the watchdog,
 * which only runs in RELEASE. If a task hogs the CPU, the idle task
 * no longer runs and the watchdog resets the board.
 */
void vApplicationIdleHook(void)
{
#ifdef RELEASE
	watchdog_refresh();
#endif
}
