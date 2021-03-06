/*
 * headlights_driver.h
 *
 *  Created on: Oct 17, 2018
 *      Author: ScorpionIPX
 */

#ifndef HEADLIGHTS_DRIVER_H_
#define HEADLIGHTS_DRIVER_H_

#include "stm32f4xx_hal.h"
#include "gpio.h"


#define HEADLIGHT_PORT_LEFT GPIOE
#define HEADLIGHT_PORT_RIGHT GPIOE
#define HEADLIGHT_PIN_LEFT GPIO_PIN_11
#define HEADLIGHT_PIN_RIGHT GPIO_PIN_12

#define HEADLIGHT_LEFT_ON (HAL_GPIO_WritePin(HEADLIGHT_PORT_LEFT, HEADLIGHT_PIN_LEFT, SET))
#define HEADLIGHT_LEFT_OFF (HAL_GPIO_WritePin(HEADLIGHT_PORT_LEFT, HEADLIGHT_PIN_LEFT, RESET))

#define HEADLIGHT_RIGHT_ON (HAL_GPIO_WritePin(HEADLIGHT_PORT_RIGHT, HEADLIGHT_PIN_RIGHT, SET))
#define HEADLIGHT_RIGHT_OFF (HAL_GPIO_WritePin(HEADLIGHT_PORT_RIGHT, HEADLIGHT_PIN_RIGHT, RESET))

#define HEADLIGHTS_ON (HEADLIGHT_LEFT_ON; HEADLIGHT_RIGHT_ON)
#define HEADLIGHTS_OFF (HEADLIGHT_LEFT_OFF; HEADLIGHT_RIGHT_OFF)

void light_control_check(void);

#endif /* HEADLIGHTS_DRIVER_H_ */
