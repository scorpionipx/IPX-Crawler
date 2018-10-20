/*
 * camera_driver.h
 *
 *  Created on: Oct 20, 2018
 *      Author: ScorpionIPX
 */

#ifndef CAMERA_DRIVER_H_
#define CAMERA_DRIVER_H_

#include "gpio.h"
#include "stm32f4xx_hal.h"

#define ROTATION_REQUEST_NONE 0
#define ROTATION_REQUEST_CCW  1
#define ROTATION_REQUEST_CW   2

#define DEFAULT_ROTATION_REQUEST_COUNTER 50

#define CAMERA_ROATAION_PORT GPIOE
#define CAMERA_ROTATION_STEP_1_PIN GPIO_PIN_7
#define CAMERA_ROTATION_STEP_2_PIN GPIO_PIN_8
#define CAMERA_ROTATION_STEP_3_PIN GPIO_PIN_9
#define CAMERA_ROTATION_STEP_4_PIN GPIO_PIN_10

void init_camera_control(void);
void SET_STEPS_CAMERA_ROTATION(uint8_t steps);
void RESET_STEPS_CAMERA_ROTATION(uint8_t steps);
void camera_rotation_stop(void);
void camera_rotaion_ccw(void);
void camera_rotaion_cw(void);

uint8_t CURRENT_STEP_CAMERA_ROTATION;
uint8_t ROTATION_STEP_DELAY_MS;

uint8_t CURRENT_STEP_CAMERA_TILT;
uint8_t TILT_STEP_DELAY_MS;

uint8_t ROTATION_REQUEST;
uint8_t ROTATION_REQUEST_COUNTER;

#endif /* CAMERA_DRIVER_H_ */
