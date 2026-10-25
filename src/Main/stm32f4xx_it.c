/**
  ******************************************************************************
  * @file    stm32f4xx_it.c
  * @brief   Interrupt Service Routines.
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2024 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */


/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "stm32f4xx_it.h"
#include "global_err.h"
#include "periph_init.h"
#include "FreeRTOS.h"
#include "task.h"

extern void xPortSysTickHandler(void);

/******************************************************************************/
/*           Cortex-M4 Processor Interruption and Exception Handlers          */
/******************************************************************************/
/**
  * @brief This function handles Non maskable interrupt.
  */
void NMI_Handler(void)
{

	vGlobalErrors_globalErrorHandler(DERROR_SYSTEM_FAULT_);

}

/**
  * @brief This function handles Hard fault interrupt.
  */
void HardFault_Handler(void)
{

	vGlobalErrors_globalErrorHandler(DERROR_SYSTEM_FAULT_);
}

/**
  * @brief This function handles Memory management fault.
  */
void MemManage_Handler(void)
{

	vGlobalErrors_globalErrorHandler(DERROR_SYSTEM_FAULT_);
}

/**
  * @brief This function handles Pre-fetch fault, memory access fault.
  */
void BusFault_Handler(void)
{


	vGlobalErrors_globalErrorHandler(DERROR_SYSTEM_FAULT_);
}

/**
  * @brief This function handles Undefined instruction or illegal state.
  */
void UsageFault_Handler(void)
{

	vGlobalErrors_globalErrorHandler(DERROR_SYSTEM_FAULT_);
}

/**
  * @brief This function handles System service call via SWI instruction.
  */

/* SVC_Handler is implemented by FreeRTOS port.c */
/* void SVC_Handler(void) {} */

/**
  * @brief This function handles Debug monitor.
  */
void DebugMon_Handler(void)
{
  /* USER CODE BEGIN DebugMonitor_IRQn 0 */

  /* USER CODE END DebugMonitor_IRQn 0 */
  /* USER CODE BEGIN DebugMonitor_IRQn 1 */

  /* USER CODE END DebugMonitor_IRQn 1 */
}

/**
  * @brief This function handles Pendable request for system service.
  */

/* PendSV_Handler is implemented by FreeRTOS port.c */
/* void PendSV_Handler(void) {} */

/**
  * @brief This function handles System tick timer.
  *        SysTick is shared: it drives the HAL time base (HAL_GetTick, timeouts)
  *        and the FreeRTOS tick once the scheduler is running.
  *        (USE_CUSTOM_SYSTICK_HANDLER_IMPLEMENTATION = 1 in FreeRTOSConfig.h)
  */
void SysTick_Handler(void)
{
  HAL_IncTick();

  if (xTaskGetSchedulerState() != taskSCHEDULER_NOT_STARTED)
  {
    xPortSysTickHandler();
  }
}

/******************************************************************************/
/* STM32F4xx Peripheral Interrupt Handlers                                    */
/* Add here the Interrupt Handlers for the used peripherals.                  */
/* For the available peripheral interrupt handler names,                      */
/* please refer to the startup file (startup_stm32f4xx.s).                    */
/******************************************************************************/

/**
  * @brief This function handles EXTI line0 interrupt.
  */
void EXTI0_IRQHandler(void)
{
  /* USER CODE END EXTI0_IRQn 0 */
  HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_0);
  /* USER CODE BEGIN EXTI0_IRQn 1 */

  /* USER CODE END EXTI0_IRQn 1 */
}

/**
  * @brief This function handles USART2 global interrupt.
  */
void USART2_IRQHandler(void)
{
    HAL_UART_IRQHandler(&huart2);
}

/* USER CODE BEGIN 1 */

/* USER CODE END 1 */
