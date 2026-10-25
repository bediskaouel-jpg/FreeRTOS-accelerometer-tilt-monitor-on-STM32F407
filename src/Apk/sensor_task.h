/*
 * sensor_task.h
 *
 */

#include <stdint.h>

#ifndef APK_SENSOR_TASK_H_
#define APK_SENSOR_TASK_H_


typedef struct
{
	int16_t X;
	int16_t Y;
}SensorData;

void SensorTask( void * pvParameters );

#endif /* APK_SENSOR_TASK_H_ */
