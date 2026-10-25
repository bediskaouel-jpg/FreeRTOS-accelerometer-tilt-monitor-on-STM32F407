/*
 *         watchdog.h
 */

#ifndef BSP_WATCHDOG_H_
#define BSP_WATCHDOG_H_
#include "stdint.h"

uint8_t watchdog_init(void);
uint8_t watchdog_refresh(void);

#endif /* BSP_WATCHDOG_H_ */
