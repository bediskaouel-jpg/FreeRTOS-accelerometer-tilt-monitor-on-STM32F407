################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (14.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../extern/BSP/STM32F4-Discovery/stm32f4_discovery.c \
../extern/BSP/STM32F4-Discovery/stm32f4_discovery_accelerometer.c 

OBJS += \
./extern/BSP/STM32F4-Discovery/stm32f4_discovery.o \
./extern/BSP/STM32F4-Discovery/stm32f4_discovery_accelerometer.o 

C_DEPS += \
./extern/BSP/STM32F4-Discovery/stm32f4_discovery.d \
./extern/BSP/STM32F4-Discovery/stm32f4_discovery_accelerometer.d 


# Each subdirectory must supply rules for building sources it contributes
extern/BSP/STM32F4-Discovery/%.o extern/BSP/STM32F4-Discovery/%.su extern/BSP/STM32F4-Discovery/%.cyclo: ../extern/BSP/STM32F4-Discovery/%.c extern/BSP/STM32F4-Discovery/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F407xx -c -I../src/Main/Inc -I../src/Middleware/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM4F -I../src/Middleware/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2 -I../src/Middleware/Third_Party/FreeRTOS/Source/include -I../extern/Drivers/STM32F4xx_HAL_Driver/Inc -I../extern/Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../extern/Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I../extern/Drivers/CMSIS/Include -I../extern/BSP/STM32F4-Discovery/ -I../extern/BSP/Components/ -I../src/global_err -I../src/util -I../src/BSP -I../src/Apk -I../src/Middleware/Third_Party/FreeRTOS/Source -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-extern-2f-BSP-2f-STM32F4-2d-Discovery

clean-extern-2f-BSP-2f-STM32F4-2d-Discovery:
	-$(RM) ./extern/BSP/STM32F4-Discovery/stm32f4_discovery.cyclo ./extern/BSP/STM32F4-Discovery/stm32f4_discovery.d ./extern/BSP/STM32F4-Discovery/stm32f4_discovery.o ./extern/BSP/STM32F4-Discovery/stm32f4_discovery.su ./extern/BSP/STM32F4-Discovery/stm32f4_discovery_accelerometer.cyclo ./extern/BSP/STM32F4-Discovery/stm32f4_discovery_accelerometer.d ./extern/BSP/STM32F4-Discovery/stm32f4_discovery_accelerometer.o ./extern/BSP/STM32F4-Discovery/stm32f4_discovery_accelerometer.su

.PHONY: clean-extern-2f-BSP-2f-STM32F4-2d-Discovery

