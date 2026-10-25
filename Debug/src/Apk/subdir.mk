################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (14.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../src/Apk/led_task.c \
../src/Apk/main_apk.c \
../src/Apk/sensor_task.c \
../src/Apk/uart_task.c 

OBJS += \
./src/Apk/led_task.o \
./src/Apk/main_apk.o \
./src/Apk/sensor_task.o \
./src/Apk/uart_task.o 

C_DEPS += \
./src/Apk/led_task.d \
./src/Apk/main_apk.d \
./src/Apk/sensor_task.d \
./src/Apk/uart_task.d 


# Each subdirectory must supply rules for building sources it contributes
src/Apk/%.o src/Apk/%.su src/Apk/%.cyclo: ../src/Apk/%.c src/Apk/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F407xx -c -I../src/Main/Inc -I../src/Middleware/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM4F -I../src/Middleware/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2 -I../src/Middleware/Third_Party/FreeRTOS/Source/include -I../extern/Drivers/STM32F4xx_HAL_Driver/Inc -I../extern/Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../extern/Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I../extern/Drivers/CMSIS/Include -I../extern/BSP/STM32F4-Discovery/ -I../extern/BSP/Components/ -I../src/global_err -I../src/util -I../src/BSP -I../src/Apk -I../src/Middleware/Third_Party/FreeRTOS/Source -O0 -ffunction-sections -fdata-sections -Wall -Wextra -Werror -pedantic -pedantic-errors -Wmissing-include-dirs -Wswitch-default -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-src-2f-Apk

clean-src-2f-Apk:
	-$(RM) ./src/Apk/led_task.cyclo ./src/Apk/led_task.d ./src/Apk/led_task.o ./src/Apk/led_task.su ./src/Apk/main_apk.cyclo ./src/Apk/main_apk.d ./src/Apk/main_apk.o ./src/Apk/main_apk.su ./src/Apk/sensor_task.cyclo ./src/Apk/sensor_task.d ./src/Apk/sensor_task.o ./src/Apk/sensor_task.su ./src/Apk/uart_task.cyclo ./src/Apk/uart_task.d ./src/Apk/uart_task.o ./src/Apk/uart_task.su

.PHONY: clean-src-2f-Apk

