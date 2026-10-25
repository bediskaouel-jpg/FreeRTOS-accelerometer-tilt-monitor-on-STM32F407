/*
 *         led.c
 */

#include "led.h"

#include "../../extern/Drivers/STM32F4xx_HAL_Driver/Inc/stm32f4xx_hal.h"

/** @defgroup BSP_LED_DRV BSP LED DRV
 * @ingroup BSP_LED_DRV
 * @brief The LED DRV file is responsible for implementing the functionality defined by the module.
 * @{
 */




/*
 *
 */
void led_init(void)
{
	  GPIO_InitTypeDef GPIO_InitStruct = {0};

	  __HAL_RCC_GPIOD_CLK_ENABLE();

	  /*Configure GPIO pin Output Level */
	  HAL_GPIO_WritePin(GPIOD, GPIO_PIN_12|GPIO_PIN_13|GPIO_PIN_14|GPIO_PIN_15, GPIO_PIN_RESET);

	  /*Configure GPIO pins : PD12 PD13 PD14 PD15 */
	  GPIO_InitStruct.Pin = GPIO_PIN_12|GPIO_PIN_13|GPIO_PIN_14|GPIO_PIN_15;
	  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
	  GPIO_InitStruct.Pull = GPIO_NOPULL;
	  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	  HAL_GPIO_Init(GPIOD, &GPIO_InitStruct);

}
/**
  * @brief  This function set the red control
  * @retval None
  */
void led_red_control(LedStatus status)
{
	if (status==LED_SET)
	{
		HAL_GPIO_WritePin(GPIOD, GPIO_PIN_14,GPIO_PIN_SET);
	}
	else
	{
		HAL_GPIO_WritePin(GPIOD, GPIO_PIN_14,GPIO_PIN_RESET);
	}


}
/**
  * @brief  This function set the green control
  * @retval None
  */
void led_green_control(LedStatus status )
{
	if (status==LED_SET)
	{
		HAL_GPIO_WritePin(GPIOD, GPIO_PIN_12,GPIO_PIN_SET);
	}
	else
	{
      HAL_GPIO_WritePin(GPIOD, GPIO_PIN_12,GPIO_PIN_RESET);
	}

}
/**
  * @brief  This function set the blue control
  * @retval None
  */
void led_blue_control(LedStatus status )
{
	if (status==LED_SET)
	{
		HAL_GPIO_WritePin(GPIOD, GPIO_PIN_15,GPIO_PIN_SET);
	}
	else
	{
		HAL_GPIO_WritePin(GPIOD, GPIO_PIN_15,GPIO_PIN_RESET);
	}

}
/**
 *
 */
void led_orange_control(LedStatus status )
{

	if (status==LED_SET)
	{
		HAL_GPIO_WritePin(GPIOD, GPIO_PIN_13,GPIO_PIN_SET);
	}
	else
	{
		HAL_GPIO_WritePin(GPIOD, GPIO_PIN_13,GPIO_PIN_RESET);
	}
}

/**
 * @}
 */
