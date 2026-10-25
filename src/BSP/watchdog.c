/*
 *         watchdog.c
 */


#include "watchdog.h"

#include "../../extern/Drivers/STM32F4xx_HAL_Driver/Inc/stm32f4xx_hal.h"


IWDG_HandleTypeDef hiwdg;


/**
 *
 */
uint8_t watchdog_init(void)
{
	uint8_t ret=0;
	  hiwdg.Instance = IWDG;
	  hiwdg.Init.Prescaler = IWDG_PRESCALER_256;
	  hiwdg.Init.Reload = 4000;
	  if (HAL_IWDG_Init(&hiwdg) != HAL_OK)
	  {
	    ret =1;
	  }
	  return ret;

}

/**
 * *
 */
uint8_t watchdog_refresh(void)
{
	HAL_IWDG_Refresh(&hiwdg);
	return 0;
}
