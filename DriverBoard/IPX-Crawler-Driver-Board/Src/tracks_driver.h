/*
 * tracks_driver.h
 *
 *  Created on: May 12, 2018
 *      Author: ScorpionIPX
 */

#ifndef TRACKS_DRIVER_H_
#define TRACKS_DRIVER_H_

#include "tim.h"
#define FL_TRACK TIM_CHANNEL_1
#define FR_TRACK TIM_CHANNEL_2
#define RL_TRACK TIM_CHANNEL_3
#define RR_TRACK TIM_CHANNEL_4

#define FL_TRACK_DIRECTION_FORWARD -1
#define FR_TRACK_DIRECTION_FORWARD -1
#define RL_TRACK_DIRECTION_FORWARD -1
#define RR_TRACK_DIRECTION_FORWARD -1

#define FL_TRACK_DIRECTION_BACKWARD -1
#define FR_TRACK_DIRECTION_BACKWARD -1
#define RL_TRACK_DIRECTION_BACKWARD -1
#define RR_TRACK_DIRECTION_BACKWARD -1

#define TRACKS_PWM_TIMER &htim4

#define SET_FL_TRACK_DIRECTION_FORWARD ()


void set_fl_track_dc(uint8_t duty_cycle);
void set_fr_track_dc(uint8_t duty_cycle);
void set_rl_track_dc(uint8_t duty_cycle);
void set_rr_track_dc(uint8_t duty_cycle);

#endif /* TRACKS_DRIVER_H_ */
