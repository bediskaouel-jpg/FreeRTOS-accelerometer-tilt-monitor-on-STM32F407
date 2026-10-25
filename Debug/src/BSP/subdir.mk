################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (14.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../src/BSP/accelero.c \
../src/BSP/autotest.c \
../src/BSP/led.c \
../src/BSP/periph_init.c \
../src/BSP/watchdog.c 

OBJS += \
./src/BSP/accelero.o \
./src/BSP/autotest.o \
./src/BSP/led.o \
./src/BSP/periph_init.o \
./src/BSP/watchdog.o 

C_DEPS += \
./src/BSP/accelero.d \
./src/BSP/autotest.d \
./src/BSP/led.d \
./src/BSP/periph_init.d \
./src/BSP/watchdog.d 


# Each subdirectory must supply rules for building sources it contributes
src/BSP/%.o src/BSP/%.su src/BSP/%.cyclo: ../src/BSP/%.c src/BSP/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F407xx -c -I../src/Main/Inc -I../src/Middleware/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM4F -I../src/Middleware/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2 -I../src/Middleware/Third_Party/FreeRTOS/Source/include -I../extern/Drivers/STM32F4xx_HAL_Driver/Inc -I../extern/Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../extern/Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I../extern/Drivers/CMSIS/Include -I../extern/BSP/STM32F4-Discovery/ -I../extern/BSP/Components/ -I../src/global_err -I../src/util -I../src/BSP -I../src/Apk -I../src/Middleware/Third_Party/FreeRTOS/Source -O0 -ffunction-sections -fdata-sections -Wall -Wextra -Werror -pedantic -pedantic-errors -Wmissing-include-dirs -Wswitch-default -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-src-2f-BSP

clean-src-2f-BSP:
	-$(RM) ./src/BSP/accelero.cyclo ./src/BSP/accelero.d ./src/BSP/accelero.o ./src/BSP/accelero.su ./src/BSP/autotest.cyclo ./src/BSP/autotest.d ./src/BSP/autotest.o ./src/BSP/autotest.su ./src/BSP/led.cyclo ./src/BSP/led.d ./src/BSP/led.o ./src/BSP/led.su ./src/BSP/periph_init.cyclo ./src/BSP/periph_init.d ./src/BSP/periph_init.o ./src/BSP/periph_init.su ./src/BSP/watchdog.cyclo ./src/BSP/watchdog.d ./src/BSP/watchdog.o ./src/BSP/watchdog.su

.PHONY: clean-src-2f-BSP

