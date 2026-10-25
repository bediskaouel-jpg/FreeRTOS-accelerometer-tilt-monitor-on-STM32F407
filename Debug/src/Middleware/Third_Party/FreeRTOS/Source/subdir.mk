################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (14.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../src/Middleware/Third_Party/FreeRTOS/Source/croutine.c \
../src/Middleware/Third_Party/FreeRTOS/Source/event_groups.c \
../src/Middleware/Third_Party/FreeRTOS/Source/list.c \
../src/Middleware/Third_Party/FreeRTOS/Source/queue.c \
../src/Middleware/Third_Party/FreeRTOS/Source/stream_buffer.c \
../src/Middleware/Third_Party/FreeRTOS/Source/tasks.c \
../src/Middleware/Third_Party/FreeRTOS/Source/timers.c 

OBJS += \
./src/Middleware/Third_Party/FreeRTOS/Source/croutine.o \
./src/Middleware/Third_Party/FreeRTOS/Source/event_groups.o \
./src/Middleware/Third_Party/FreeRTOS/Source/list.o \
./src/Middleware/Third_Party/FreeRTOS/Source/queue.o \
./src/Middleware/Third_Party/FreeRTOS/Source/stream_buffer.o \
./src/Middleware/Third_Party/FreeRTOS/Source/tasks.o \
./src/Middleware/Third_Party/FreeRTOS/Source/timers.o 

C_DEPS += \
./src/Middleware/Third_Party/FreeRTOS/Source/croutine.d \
./src/Middleware/Third_Party/FreeRTOS/Source/event_groups.d \
./src/Middleware/Third_Party/FreeRTOS/Source/list.d \
./src/Middleware/Third_Party/FreeRTOS/Source/queue.d \
./src/Middleware/Third_Party/FreeRTOS/Source/stream_buffer.d \
./src/Middleware/Third_Party/FreeRTOS/Source/tasks.d \
./src/Middleware/Third_Party/FreeRTOS/Source/timers.d 


# Each subdirectory must supply rules for building sources it contributes
src/Middleware/Third_Party/FreeRTOS/Source/%.o src/Middleware/Third_Party/FreeRTOS/Source/%.su src/Middleware/Third_Party/FreeRTOS/Source/%.cyclo: ../src/Middleware/Third_Party/FreeRTOS/Source/%.c src/Middleware/Third_Party/FreeRTOS/Source/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F407xx -c -I../src/Main/Inc -I../src/Middleware/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM4F -I../src/Middleware/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2 -I../src/Middleware/Third_Party/FreeRTOS/Source/include -I../extern/Drivers/STM32F4xx_HAL_Driver/Inc -I../extern/Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../extern/Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I../extern/Drivers/CMSIS/Include -I../extern/BSP/STM32F4-Discovery/ -I../extern/BSP/Components/ -I../src/global_err -I../src/util -I../src/BSP -I../src/Apk -I../src/Middleware/Third_Party/FreeRTOS/Source -O0 -ffunction-sections -fdata-sections -Wall -Wextra -Werror -pedantic -pedantic-errors -Wmissing-include-dirs -Wswitch-default -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-src-2f-Middleware-2f-Third_Party-2f-FreeRTOS-2f-Source

clean-src-2f-Middleware-2f-Third_Party-2f-FreeRTOS-2f-Source:
	-$(RM) ./src/Middleware/Third_Party/FreeRTOS/Source/croutine.cyclo ./src/Middleware/Third_Party/FreeRTOS/Source/croutine.d ./src/Middleware/Third_Party/FreeRTOS/Source/croutine.o ./src/Middleware/Third_Party/FreeRTOS/Source/croutine.su ./src/Middleware/Third_Party/FreeRTOS/Source/event_groups.cyclo ./src/Middleware/Third_Party/FreeRTOS/Source/event_groups.d ./src/Middleware/Third_Party/FreeRTOS/Source/event_groups.o ./src/Middleware/Third_Party/FreeRTOS/Source/event_groups.su ./src/Middleware/Third_Party/FreeRTOS/Source/list.cyclo ./src/Middleware/Third_Party/FreeRTOS/Source/list.d ./src/Middleware/Third_Party/FreeRTOS/Source/list.o ./src/Middleware/Third_Party/FreeRTOS/Source/list.su ./src/Middleware/Third_Party/FreeRTOS/Source/queue.cyclo ./src/Middleware/Third_Party/FreeRTOS/Source/queue.d ./src/Middleware/Third_Party/FreeRTOS/Source/queue.o ./src/Middleware/Third_Party/FreeRTOS/Source/queue.su ./src/Middleware/Third_Party/FreeRTOS/Source/stream_buffer.cyclo ./src/Middleware/Third_Party/FreeRTOS/Source/stream_buffer.d ./src/Middleware/Third_Party/FreeRTOS/Source/stream_buffer.o ./src/Middleware/Third_Party/FreeRTOS/Source/stream_buffer.su ./src/Middleware/Third_Party/FreeRTOS/Source/tasks.cyclo ./src/Middleware/Third_Party/FreeRTOS/Source/tasks.d ./src/Middleware/Third_Party/FreeRTOS/Source/tasks.o ./src/Middleware/Third_Party/FreeRTOS/Source/tasks.su ./src/Middleware/Third_Party/FreeRTOS/Source/timers.cyclo ./src/Middleware/Third_Party/FreeRTOS/Source/timers.d ./src/Middleware/Third_Party/FreeRTOS/Source/timers.o ./src/Middleware/Third_Party/FreeRTOS/Source/timers.su

.PHONY: clean-src-2f-Middleware-2f-Third_Party-2f-FreeRTOS-2f-Source

