/*
 * tracks_driver.c
 *
 *  Created on: May 12, 2018
 *      Author: ScorpionIPX
 */


#include "gpio.h"
#include "stm32f4xx_hal.h"
#include "tim.h"
#include "tracks_driver.h"


void dummy(void)
{

}

void set_fl_track_dc(uint8_t duty_cycle)
{
	__HAL_TIM_SET_COMPARE(TRACKS_PWM_TIMER, FL_TRACK, duty_cycle);
}

void set_fr_track_dc(uint8_t duty_cycle)
{
	__HAL_TIM_SET_COMPARE(TRACKS_PWM_TIMER, FR_TRACK, duty_cycle);
}

void set_rl_track_dc(uint8_t duty_cycle)
{
	__HAL_TIM_SET_COMPARE(TRACKS_PWM_TIMER, RL_TRACK, duty_cycle);
}

void set_rr_track_dc(uint8_t duty_cycle)
{
	__HAL_TIM_SET_COMPARE(TRACKS_PWM_TIMER, RR_TRACK, duty_cycle);
}

void fl_track_forward(uint8_t speed)
{
	HAL_GPIO_WritePin(FL_TRACK_DIRECTION_PORT, FL_TRACK_DIRECTION_BACKWARD_PIN, 0);
	HAL_GPIO_WritePin(FL_TRACK_DIRECTION_PORT, FL_TRACK_DIRECTION_FORWARD_PIN, 1);
	set_fl_track_dc(speed);
}

void fl_track_backward(uint8_t speed)
{
	HAL_GPIO_WritePin(FL_TRACK_DIRECTION_PORT, FL_TRACK_DIRECTION_FORWARD_PIN, 0);
	HAL_GPIO_WritePin(FL_TRACK_DIRECTION_PORT, FL_TRACK_DIRECTION_BACKWARD_PIN, 1);
	set_fl_track_dc(speed);
}

void fr_track_forward(uint8_t speed)
{
	HAL_GPIO_WritePin(FR_TRACK_DIRECTION_PORT, FR_TRACK_DIRECTION_BACKWARD_PIN, 0);
	HAL_GPIO_WritePin(FR_TRACK_DIRECTION_PORT, FR_TRACK_DIRECTION_FORWARD_PIN, 1);
	set_fr_track_dc(speed);
}

void fr_track_backward(uint8_t speed)
{
	HAL_GPIO_WritePin(FR_TRACK_DIRECTION_PORT, FR_TRACK_DIRECTION_FORWARD_PIN, 0);
	HAL_GPIO_WritePin(FR_TRACK_DIRECTION_PORT, FR_TRACK_DIRECTION_BACKWARD_PIN, 1);
	set_fr_track_dc(speed);
}


void rl_track_forward(uint8_t speed)
{
	HAL_GPIO_WritePin(RL_TRACK_DIRECTION_PORT, RL_TRACK_DIRECTION_BACKWARD_PIN, 0);
	HAL_GPIO_WritePin(RL_TRACK_DIRECTION_PORT, RL_TRACK_DIRECTION_FORWARD_PIN, 1);
	set_rl_track_dc(speed);
}

void rl_track_backward(uint8_t speed)
{
	HAL_GPIO_WritePin(RL_TRACK_DIRECTION_PORT, RL_TRACK_DIRECTION_FORWARD_PIN, 0);
	HAL_GPIO_WritePin(RL_TRACK_DIRECTION_PORT, RL_TRACK_DIRECTION_BACKWARD_PIN, 1);
	set_rl_track_dc(speed);
}

void rr_track_forward(uint8_t speed)
{
	HAL_GPIO_WritePin(RR_TRACK_DIRECTION_PORT, RR_TRACK_DIRECTION_BACKWARD_PIN, 0);
	HAL_GPIO_WritePin(RR_TRACK_DIRECTION_PORT, RR_TRACK_DIRECTION_FORWARD_PIN, 1);
	set_rr_track_dc(speed);
}

void rr_track_backward(uint8_t speed)
{
	HAL_GPIO_WritePin(RR_TRACK_DIRECTION_PORT, RR_TRACK_DIRECTION_FORWARD_PIN, 0);
	HAL_GPIO_WritePin(RR_TRACK_DIRECTION_PORT, RR_TRACK_DIRECTION_BACKWARD_PIN, 1);
	set_rr_track_dc(speed);
}

void stop_tracks(void)
{
	HAL_GPIO_WritePin(FL_TRACK_DIRECTION_PORT, FL_TRACK_DIRECTION_BACKWARD_PIN, 0);
	HAL_GPIO_WritePin(FL_TRACK_DIRECTION_PORT, FL_TRACK_DIRECTION_FORWARD_PIN, 0);
	HAL_GPIO_WritePin(FR_TRACK_DIRECTION_PORT, FR_TRACK_DIRECTION_BACKWARD_PIN, 0);
	HAL_GPIO_WritePin(FR_TRACK_DIRECTION_PORT, FR_TRACK_DIRECTION_FORWARD_PIN, 0);

	HAL_GPIO_WritePin(RL_TRACK_DIRECTION_PORT, RL_TRACK_DIRECTION_BACKWARD_PIN, 0);
	HAL_GPIO_WritePin(RL_TRACK_DIRECTION_PORT, RL_TRACK_DIRECTION_FORWARD_PIN, 0);
	HAL_GPIO_WritePin(RR_TRACK_DIRECTION_PORT, RR_TRACK_DIRECTION_BACKWARD_PIN, 0);
	HAL_GPIO_WritePin(RR_TRACK_DIRECTION_PORT, RR_TRACK_DIRECTION_FORWARD_PIN, 0);

	set_fl_track_dc(0);
	set_fr_track_dc(0);
	set_rl_track_dc(0);
	set_rr_track_dc(0);
}

void drive(uint8_t power, uint8_t steering)
{

}
