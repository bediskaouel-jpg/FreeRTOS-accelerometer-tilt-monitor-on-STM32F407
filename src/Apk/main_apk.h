/*
 * main_apk.h
 *
 */

#include <stdint.h>
#include "FreeRTOS.h"
#include "queue.h"

#ifndef APK_MAIN_APK_H_
#define APK_MAIN_APK_H_

#define SENSOR_PERIOD_MS 50

/* Stack sizes in 32-bit words. SensorTask uses the FPU (LIS3DSH driver)
 * and sends on the UART: it needs the largest stack. */
#define SENSOR_STACK_SIZE   256
#define LED_STACK_SIZE      128
#define UART_STACK_SIZE     256

#define SENSOR_PRIORITY     2
#define LED_PRIORITY        3
#define UART_PRIORITY       1
int MainApk_Init(void);

extern QueueHandle_t    SensorQueue;

#endif /* APK_MAIN_APK_H_ */
