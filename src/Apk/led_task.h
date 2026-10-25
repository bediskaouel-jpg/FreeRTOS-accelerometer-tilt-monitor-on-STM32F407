/*
 * led_task.h
 *
 */

#ifndef APK_LED_TASK_H_
#define APK_LED_TASK_H_

#include "uart_task.h"

#define LED_CMD_LEFT 0xC1
#define LED_CMD_RIGHT 0xD1
#define LED_CMD_UP 0xE1
#define LED_CMD_DOWN 0xF1

#define X_THREASH_INIT 200
#define Y_THREASH_INIT 200

#define LED_PERIOD_MS 100   /* LED refresh period: a tilted LED blinks at 5 Hz */

typedef enum
{
	LED_OFF = 0,
	LED_ON
}LedState;

void LedTask(void * pvParameters);
void ExecuteCommand(FrameUART Frame);
void LedUpdate(int16_t X_Val, int16_t Y_Val);

#endif /* APK_LED_TASK_H_ */
