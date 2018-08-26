################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Src/gpio.c \
../Src/ili9341.c \
../Src/main.c \
../Src/spi.c \
../Src/stm32f4xx_hal_msp.c \
../Src/stm32f4xx_it.c \
../Src/system_stm32f4xx.c \
../Src/tim.c \
../Src/tracks_driver.c 

OBJS += \
./Src/gpio.o \
./Src/ili9341.o \
./Src/main.o \
./Src/spi.o \
./Src/stm32f4xx_hal_msp.o \
./Src/stm32f4xx_it.o \
./Src/system_stm32f4xx.o \
./Src/tim.o \
./Src/tracks_driver.o 

C_DEPS += \
./Src/gpio.d \
./Src/ili9341.d \
./Src/main.d \
./Src/spi.d \
./Src/stm32f4xx_hal_msp.d \
./Src/stm32f4xx_it.d \
./Src/system_stm32f4xx.d \
./Src/tim.d \
./Src/tracks_driver.d 


# Each subdirectory must supply rules for building sources it contributes
Src/%.o: ../Src/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: MCU GCC Compiler'
	@echo $(PWD)
	arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16 '-D__weak=__attribute__((weak))' '-D__packed="__attribute__((__packed__))"' -DUSE_HAL_DRIVER -DSTM32F429xx '-D__weak=__attribute__((weak))' '-D__packed=__attribute__((__packed__))' -I"D:/Documents/Programming/Repositories/ipx_crawler/DriverBoard/IPX-Crawler-Driver-Board/Inc" -I"D:/Documents/Programming/Repositories/ipx_crawler/DriverBoard/IPX-Crawler-Driver-Board/Drivers/STM32F4xx_HAL_Driver/Inc" -I"D:/Documents/Programming/Repositories/ipx_crawler/DriverBoard/IPX-Crawler-Driver-Board/Drivers/STM32F4xx_HAL_Driver/Inc/Legacy" -I"D:/Documents/Programming/Repositories/ipx_crawler/DriverBoard/IPX-Crawler-Driver-Board/Drivers/CMSIS/Device/ST/STM32F4xx/Include" -I"D:/Documents/Programming/Repositories/ipx_crawler/DriverBoard/IPX-Crawler-Driver-Board/Drivers/CMSIS/Include" -I"D:/Documents/Programming/Repositories/ipx_crawler/DriverBoard/IPX-Crawler-Driver-Board/Inc"  -Og -g3 -Wall -fmessage-length=0 -ffunction-sections -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


