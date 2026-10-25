/*
 *         accelero.h
 */

#ifndef BSP_ACCELERO_H_
#define BSP_ACCELERO_H_

#include "stdint.h"
#include "stm32f4_discovery_accelerometer.h"

uint8_t acc_init(void);
uint8_t acc_getdata(int16_t *buff);



#endif /* BSP_ACCELERO_H_ */
