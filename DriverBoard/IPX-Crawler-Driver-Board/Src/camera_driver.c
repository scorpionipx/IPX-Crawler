/*
 * camera_driver.c
 *
 *  Created on: Oct 20, 2018
 *      Author: ScorpionIPX
 */


#include "camera_driver.h"
#include "gpio.h"
#include "stm32f4xx_hal.h"

#define SET_STEP_1_CAMERA_ROTATION (HAL_GPIO_MODU)

void rotate_camera()
{
	switch(ROTATION_REQUEST)
	{
		case ROTATION_REQUEST_CCW:
		{
			camera_rotaion_ccw();
			HAL_Delay(ROTATION_STEP_DELAY_MS);
			ROTATION_REQUEST_COUNTER --;
			break;
		}
		case ROTATION_REQUEST_CW:
		{
			camera_rotaion_cw();
			HAL_Delay(ROTATION_STEP_DELAY_MS);
			ROTATION_REQUEST_COUNTER --;
			break;
		}
		default:
		{
			break;
		}
	}
	if(!ROTATION_REQUEST_COUNTER)
	{
		camera_rotation_stop();
		ROTATION_REQUEST = ROTATION_REQUEST_NONE;
	}
}

void init_camera_control(void)
{
	camera_rotation_stop();

	CURRENT_STEP_CAMERA_ROTATION = 1;
	ROTATION_STEP_DELAY_MS = 4;

	CURRENT_STEP_CAMERA_TILT = 1;
	TILT_STEP_DELAY_MS = 4;

	ROTATION_REQUEST_COUNTER = DEFAULT_ROTATION_REQUEST_COUNTER;
}

void SET_STEPS_CAMERA_ROTATION(uint8_t steps)
{
	HAL_GPIO_WritePin(CAMERA_ROATAION_PORT, CAMERA_ROTATION_STEP_1_PIN, steps & 1);
	HAL_GPIO_WritePin(CAMERA_ROATAION_PORT, CAMERA_ROTATION_STEP_2_PIN, (steps >> 1) & 1);
	HAL_GPIO_WritePin(CAMERA_ROATAION_PORT, CAMERA_ROTATION_STEP_3_PIN, (steps >> 2) & 1);
	HAL_GPIO_WritePin(CAMERA_ROATAION_PORT, CAMERA_ROTATION_STEP_4_PIN, (steps >> 3) & 1);
}

void RESET_STEPS_CAMERA_ROTATION(uint8_t steps)
{
	HAL_GPIO_WritePin(CAMERA_ROATAION_PORT, CAMERA_ROTATION_STEP_1_PIN, ~steps & 1);
	HAL_GPIO_WritePin(CAMERA_ROATAION_PORT, CAMERA_ROTATION_STEP_2_PIN, (~steps >> 1) & 1);
	HAL_GPIO_WritePin(CAMERA_ROATAION_PORT, CAMERA_ROTATION_STEP_3_PIN, (~steps >> 2) & 1);
	HAL_GPIO_WritePin(CAMERA_ROATAION_PORT, CAMERA_ROTATION_STEP_4_PIN, (~steps >> 3) & 1);
}


void camera_rotation_stop(void)
{
	HAL_GPIO_WritePin(CAMERA_ROATAION_PORT, CAMERA_ROTATION_STEP_1_PIN, RESET);
	HAL_GPIO_WritePin(CAMERA_ROATAION_PORT, CAMERA_ROTATION_STEP_2_PIN, RESET);
	HAL_GPIO_WritePin(CAMERA_ROATAION_PORT, CAMERA_ROTATION_STEP_3_PIN, RESET);
	HAL_GPIO_WritePin(CAMERA_ROATAION_PORT, CAMERA_ROTATION_STEP_4_PIN, RESET);
}

void camera_rotaion_ccw(void)
{
	switch(CURRENT_STEP_CAMERA_ROTATION)
	{
		case 1:
		{
			CURRENT_STEP_CAMERA_ROTATION ++;
			SET_STEPS_CAMERA_ROTATION(1);
			break;
		}
		case 2:
		{
			CURRENT_STEP_CAMERA_ROTATION ++;
			SET_STEPS_CAMERA_ROTATION(2);
			break;
		}
		case 3:
		{
			CURRENT_STEP_CAMERA_ROTATION ++;
			SET_STEPS_CAMERA_ROTATION(4);
			break;
		}
		case 4:
		{
			CURRENT_STEP_CAMERA_ROTATION = 1;
			SET_STEPS_CAMERA_ROTATION(8);
			break;
		}
		default:
		{
			CURRENT_STEP_CAMERA_ROTATION = 1;
			break;
		}
	}
}

void camera_rotaion_cw(void)
{
	switch(CURRENT_STEP_CAMERA_ROTATION)
	{
		case 1:
		{
			CURRENT_STEP_CAMERA_ROTATION = 4;
			SET_STEPS_CAMERA_ROTATION(1);
			break;
		}
		case 2:
		{
			CURRENT_STEP_CAMERA_ROTATION --;
			SET_STEPS_CAMERA_ROTATION(2);
			break;
		}
		case 3:
		{
			CURRENT_STEP_CAMERA_ROTATION --;
			SET_STEPS_CAMERA_ROTATION(4);
			break;
		}
		case 4:
		{
			CURRENT_STEP_CAMERA_ROTATION --;
			SET_STEPS_CAMERA_ROTATION(8);
			break;
		}
		default:
		{
			CURRENT_STEP_CAMERA_ROTATION = 4;
			break;
		}
	}
}
