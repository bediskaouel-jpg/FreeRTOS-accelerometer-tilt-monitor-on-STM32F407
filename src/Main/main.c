/*
 *         main.c
 */

/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "periph_init.h"
#include "watchdog.h"
#include "autotest.h"
#include "accelero.h"
#include "global_err.h"
#include "main_apk.h"
#include <stdio.h>
/** @defgroup MAIN MAIN
 * @ingroup MAIN_MODULE
 * @brief Define the prototype and structure definition for the MAIN module
 * @{
 */
#ifdef USE_SEMIHOSTING
extern void initialise_monitor_handles(void);
#endif


uint8_t ret;

/**
 * @brief  The application entry point.
 * @param argument: Not Used
 * @return int: Program exit status
 */
int main(void)
{


#ifdef USE_SEMIHOSTING
  /* printf through the debugger (semihosting). The board hangs if it starts without
   * a debug session. To use it: define USE_SEMIHOSTING and exclude syscalls.c from
   * the build, so that librdimon (-lrdimon) provides the system calls. */
  initialise_monitor_handles();
#endif

  /*init HAL */
  HAL_Init();

  /*init periph */
  ret=periph_init();

  if (ret != 0)
  {
      vGlobalErrors_globalErrorHandler(DERROR_PERIPH_INIT_FAIL_);
  }

  /*run autotest*/
  ret=autotest_run();

  if (ret != 0)
	{
	  vGlobalErrors_globalErrorHandler(DERROR_AUTOTEST_FAIL_);
	 }

  /* Tasks Creation*/
  if (MainApk_Init() != 0)
  {
      vGlobalErrors_globalErrorHandler(DERROR_TASK_CREATION_FAIL_);
  }

	/* Run Scheduler */
	vTaskStartScheduler();

  /* Infinite loop */
  while (1)
  {
  }


}


/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/**
 * @}
 */
