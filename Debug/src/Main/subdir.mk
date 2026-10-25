################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (14.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
S_SRCS += \
../src/Main/startup_stm32f407vgtx.s 

C_SRCS += \
../src/Main/main.c \
../src/Main/stm32f4xx_hal_msp.c \
../src/Main/stm32f4xx_it.c \
../src/Main/syscalls.c \
../src/Main/sysmem.c \
../src/Main/system_stm32f4xx.c 

OBJS += \
./src/Main/main.o \
./src/Main/startup_stm32f407vgtx.o \
./src/Main/stm32f4xx_hal_msp.o \
./src/Main/stm32f4xx_it.o \
./src/Main/syscalls.o \
./src/Main/sysmem.o \
./src/Main/system_stm32f4xx.o 

S_DEPS += \
./src/Main/startup_stm32f407vgtx.d 

C_DEPS += \
./src/Main/main.d \
./src/Main/stm32f4xx_hal_msp.d \
./src/Main/stm32f4xx_it.d \
./src/Main/syscalls.d \
./src/Main/sysmem.d \
./src/Main/system_stm32f4xx.d 


# Each subdirectory must supply rules for building sources it contributes
src/Main/%.o src/Main/%.su src/Main/%.cyclo: ../src/Main/%.c src/Main/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F407xx -c -I../src/Main/Inc -I../src/Middleware/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM4F -I../src/Middleware/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2 -I../src/Middleware/Third_Party/FreeRTOS/Source/include -I../extern/Drivers/STM32F4xx_HAL_Driver/Inc -I../extern/Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../extern/Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I../extern/Drivers/CMSIS/Include -I../extern/BSP/STM32F4-Discovery/ -I../extern/BSP/Components/ -I../src/global_err -I../src/util -I../src/BSP -I../src/Apk -I../src/Middleware/Third_Party/FreeRTOS/Source -O0 -ffunction-sections -fdata-sections -Wall -Wextra -Werror -pedantic -pedantic-errors -Wmissing-include-dirs -Wswitch-default -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"
src/Main/%.o: ../src/Main/%.s src/Main/subdir.mk
	arm-none-eabi-gcc -mcpu=cortex-m4 -g3 -DDEBUG -c -x assembler-with-cpp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@" "$<"

clean: clean-src-2f-Main

clean-src-2f-Main:
	-$(RM) ./src/Main/main.cyclo ./src/Main/main.d ./src/Main/main.o ./src/Main/main.su ./src/Main/startup_stm32f407vgtx.d ./src/Main/startup_stm32f407vgtx.o ./src/Main/stm32f4xx_hal_msp.cyclo ./src/Main/stm32f4xx_hal_msp.d ./src/Main/stm32f4xx_hal_msp.o ./src/Main/stm32f4xx_hal_msp.su ./src/Main/stm32f4xx_it.cyclo ./src/Main/stm32f4xx_it.d ./src/Main/stm32f4xx_it.o ./src/Main/stm32f4xx_it.su ./src/Main/syscalls.cyclo ./src/Main/syscalls.d ./src/Main/syscalls.o ./src/Main/syscalls.su ./src/Main/sysmem.cyclo ./src/Main/sysmem.d ./src/Main/sysmem.o ./src/Main/sysmem.su ./src/Main/system_stm32f4xx.cyclo ./src/Main/system_stm32f4xx.d ./src/Main/system_stm32f4xx.o ./src/Main/system_stm32f4xx.su

.PHONY: clean-src-2f-Main

