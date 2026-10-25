/*
 *         periph_init.h
 */


#ifndef BSP_PERIPH_INIT_H_
#define BSP_PERIPH_INIT_H_

#include "stdint.h"
#include "stm32f4xx_hal.h"
#include "cmsis_os.h"

extern I2C_HandleTypeDef hi2c1;
extern SPI_HandleTypeDef hspi1;
extern TIM_HandleTypeDef htim2;
extern UART_HandleTypeDef huart2;

uint8_t periph_init(void);


#endif /* BSP_PERIPH_INIT_H_ */
