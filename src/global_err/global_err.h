/*
 *         global_err.h
 */

#ifndef GLOBAL_ERR_H_
#define GLOBAL_ERR_H_

/*Include -----------------------------------------*/
#include "stdint.h"



/*ERROR CODE */
#define DERROR_TASK_CREATION_FAIL_                   1U
#define DERROR_QUEUE_CREATION_FAIL_                  2U
#define DERROR_SYSTEM_CLOCK_FAIL_                    3U
#define DERROR_PERIPH_INIT_FAIL_                     4U
#define DERROR_SYSTEM_FAULT_                         5U
#define DERROR_OVERSTACK_FAIL_                       6U
#define DERROR_HAL_API_FAIL_                         7U
#define DERROR_NO_TASK_FOUND_FAIL                    8U
#define DERROR_BSP_INIT_FAIL                         9U
#define DERROR_AUTOTEST_FAIL_                       10U



/**
 * @brief Global error handler function
 * @param errorCode: Error code indicating the specific error encountered
 * @return None
 * @note This function handles global errors based on the provided error code.
 *       It switches on the error code and performs specific actions for each case.
 */
void vGlobalErrors_globalErrorHandler( uint16_t errorCode );






#endif /* GLOBAL_ERR_H_ */
