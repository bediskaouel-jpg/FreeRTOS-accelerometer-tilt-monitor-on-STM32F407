################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (14.3.rel1)
################################################################################

-include ../makefile.init

RM := rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include src/global_err/subdir.mk
-include src/Middleware/Third_Party/FreeRTOS/Source/portable/MemMang/subdir.mk
-include src/Middleware/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM4F/subdir.mk
-include src/Middleware/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/subdir.mk
-include src/Middleware/Third_Party/FreeRTOS/Source/subdir.mk
-include src/Main/subdir.mk
-include src/BSP/subdir.mk
-include src/Apk/subdir.mk
-include extern/Drivers/STM32F4xx_HAL_Driver/Src/subdir.mk
-include extern/BSP/STM32F4-Discovery/subdir.mk
-include extern/BSP/Components/lsm303dlhc/subdir.mk
-include extern/BSP/Components/lis3dsh/subdir.mk
-include extern/BSP/Components/lis302dl/subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(S_DEPS)),)
-include $(S_DEPS)
endif
ifneq ($(strip $(S_UPPER_DEPS)),)
-include $(S_UPPER_DEPS)
endif
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
endif

-include ../makefile.defs

OPTIONAL_TOOL_DEPS := \
$(wildcard ../makefile.defs) \
$(wildcard ../makefile.init) \
$(wildcard ../makefile.targets) \


BUILD_ARTIFACT_NAME := FreeRTOS Accelero Project
BUILD_ARTIFACT_EXTENSION := elf
BUILD_ARTIFACT_PREFIX :=
BUILD_ARTIFACT := $(BUILD_ARTIFACT_PREFIX)$(BUILD_ARTIFACT_NAME)$(if $(BUILD_ARTIFACT_EXTENSION),.$(BUILD_ARTIFACT_EXTENSION),)

# Add inputs and outputs from these tool invocations to the build variables 
EXECUTABLES += \
FreeRTOS\ Accelero\ Project.elf \

MAP_FILES += \
FreeRTOS\ Accelero\ Project.map \

SIZE_OUTPUT += \
default.size.stdout \

OBJDUMP_LIST += \
FreeRTOS\ Accelero\ Project.list \


# All Target
all: main-build

# Main-build Target
main-build: FreeRTOS\ Accelero\ Project.elf secondary-outputs

# Tool invocations
FreeRTOS\ Accelero\ Project.elf FreeRTOS\ Accelero\ Project.map: $(OBJS) $(USER_OBJS) C:/Users/USER/Desktop/Embeded_Projects/STM32/STM32\ F4/Perso\ Labs/FreeRTOS\ Project/project_template/Claude\ Fixe/STM32F407VGTX_FLASH.ld makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-gcc -o "FreeRTOS Accelero Project.elf" @"objects.list" $(USER_OBJS) $(LIBS) -mcpu=cortex-m4 -T"C:/Users/USER/Desktop/Embeded_Projects/STM32/STM32 F4/Perso Labs/FreeRTOS Project/project_template/Claude Fixe/STM32F407VGTX_FLASH.ld" --specs=nosys.specs -Wl,-Map="FreeRTOS Accelero Project.map" -Wl,--gc-sections -static -L--specs=rdimon.specs --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -Wl,--start-group -lc -lm -Wl,--end-group
	@echo 'Finished building target: $@'
	@echo ' '

default.size.stdout: $(EXECUTABLES) makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-size  $(EXECUTABLES)
	@echo 'Finished building: $@'
	@echo ' '

FreeRTOS\ Accelero\ Project.list: $(EXECUTABLES) makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-objdump -h -S $(EXECUTABLES) > "FreeRTOS Accelero Project.list"
	@echo 'Finished building: $@'
	@echo ' '

# Other Targets
clean:
	-$(RM) FreeRTOS\ Accelero\ Project.elf FreeRTOS\ Accelero\ Project.list FreeRTOS\ Accelero\ Project.map FreeRTOS\\ Accelero\\ Project.elf default.size.stdout
	-@echo ' '

secondary-outputs: $(SIZE_OUTPUT) $(OBJDUMP_LIST)

fail-specified-linker-script-missing:
	@echo 'Error: Cannot find the specified linker script. Check the linker settings in the build configuration.'
	@exit 2

warn-no-linker-script-specified:
	@echo 'Warning: No linker script specified. Check the linker settings in the build configuration.'

.PHONY: all clean dependents main-build fail-specified-linker-script-missing warn-no-linker-script-specified

-include ../makefile.targets
