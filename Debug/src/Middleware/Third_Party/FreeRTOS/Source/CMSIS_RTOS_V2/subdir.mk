################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (14.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../src/Middleware/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/cmsis_os2.c 

OBJS += \
./src/Middleware/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/cmsis_os2.o 

C_DEPS += \
./src/Middleware/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/cmsis_os2.d 


# Each subdirectory must supply rules for building sources it contributes
src/Middleware/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/%.o src/Middleware/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/%.su src/Middleware/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/%.cyclo: ../src/Middleware/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/%.c src/Middleware/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F407xx -c -I../src/Main/Inc -I../src/Middleware/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM4F -I../src/Middleware/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2 -I../src/Middleware/Third_Party/FreeRTOS/Source/include -I../extern/Drivers/STM32F4xx_HAL_Driver/Inc -I../extern/Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../extern/Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I../extern/Drivers/CMSIS/Include -I../extern/BSP/STM32F4-Discovery/ -I../extern/BSP/Components/ -I../src/global_err -I../src/util -I../src/BSP -I../src/Apk -I../src/Middleware/Third_Party/FreeRTOS/Source -O0 -ffunction-sections -fdata-sections -Wall -Wextra -Werror -pedantic -pedantic-errors -Wmissing-include-dirs -Wswitch-default -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-src-2f-Middleware-2f-Third_Party-2f-FreeRTOS-2f-Source-2f-CMSIS_RTOS_V2

clean-src-2f-Middleware-2f-Third_Party-2f-FreeRTOS-2f-Source-2f-CMSIS_RTOS_V2:
	-$(RM) ./src/Middleware/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/cmsis_os2.cyclo ./src/Middleware/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/cmsis_os2.d ./src/Middleware/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/cmsis_os2.o ./src/Middleware/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/cmsis_os2.su

.PHONY: clean-src-2f-Middleware-2f-Third_Party-2f-FreeRTOS-2f-Source-2f-CMSIS_RTOS_V2

