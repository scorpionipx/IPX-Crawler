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

void drive(uint8_t power, uint8_t steering)
{

}
