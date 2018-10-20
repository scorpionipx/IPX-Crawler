/*
 * tracks_driver.h
 *
 *  Created on: May 12, 2018
 *      Author: ScorpionIPX
 */

#ifndef TRACKS_DRIVER_H_
#define TRACKS_DRIVER_H_

#include "tim.h"

#define FL_TRACK 0
#define FR_TRACK 1
#define RL_TRACK 2
#define RR_TRACK 3

#define FL_TRACK_TIMER_CHANNEL TIM_CHANNEL_1
#define FR_TRACK_TIMER_CHANNEL TIM_CHANNEL_2
#define RL_TRACK_TIMER_CHANNEL TIM_CHANNEL_3
#define RR_TRACK_TIMER_CHANNEL TIM_CHANNEL_4

#define TRACK_DIRECTION_NONE 0
#define TRACK_DIRECTION_FORWARD 1
#define TRACK_DIRECTION_BACKWARD 2

#define FL_TRACK_DIRECTION_FORWARD -1
#define FR_TRACK_DIRECTION_FORWARD -1
#define RL_TRACK_DIRECTION_FORWARD -1
#define RR_TRACK_DIRECTION_FORWARD -1

#define FL_TRACK_DIRECTION_BACKWARD -1
#define FR_TRACK_DIRECTION_BACKWARD -1
#define RL_TRACK_DIRECTION_BACKWARD -1
#define RR_TRACK_DIRECTION_BACKWARD -1

#define TRACKS_PWM_TIMER &htim4

#define FL_TRACK_DIRECTION_PORT GPIOD
#define FL_TRACK_DIRECTION_FORWARD_PIN GPIO_PIN_2
#define FL_TRACK_DIRECTION_BACKWARD_PIN GPIO_PIN_3

#define FR_TRACK_DIRECTION_PORT GPIOD
#define FR_TRACK_DIRECTION_FORWARD_PIN GPIO_PIN_4
#define FR_TRACK_DIRECTION_BACKWARD_PIN GPIO_PIN_5

#define RL_TRACK_DIRECTION_PORT GPIOD
#define RL_TRACK_DIRECTION_FORWARD_PIN GPIO_PIN_0
#define RL_TRACK_DIRECTION_BACKWARD_PIN GPIO_PIN_1

#define RR_TRACK_DIRECTION_PORT GPIOC
#define RR_TRACK_DIRECTION_FORWARD_PIN GPIO_PIN_11
#define RR_TRACK_DIRECTION_BACKWARD_PIN GPIO_PIN_12

void init_tracks_control(void);

void set_fl_track_direction(unsigned short direction);
void set_fl_track_direction_forward(void);
void set_fl_track_direction_backward(void);
void set_fl_track_direction_none(void);

void set_fr_track_direction(unsigned short direction);
void set_fr_track_direction_forward(void);
void set_fr_track_direction_backward(void);
void set_fr_track_direction_none(void);

void set_rl_track_direction(unsigned short direction);
void set_rl_track_direction_forward(void);
void set_rl_track_direction_backward(void);
void set_rl_track_direction_none(void);

void set_rr_track_direction(unsigned short direction);
void set_rr_track_direction_forward(void);
void set_rr_track_direction_backward(void);
void set_rr_track_direction_none(void);

void set_track_direction(unsigned short track, unsigned short direction);

void set_fl_track_dc(uint8_t duty_cycle);
void set_fr_track_dc(uint8_t duty_cycle);
void set_rl_track_dc(uint8_t duty_cycle);
void set_rr_track_dc(uint8_t duty_cycle);

void fl_track_forkward(uint8_t speed);
void fl_track_backward(uint8_t speed);
void fr_track_forkward(uint8_t speed);
void fr_track_backward(uint8_t speed);

void rl_track_forkward(uint8_t speed);
void rl_track_backward(uint8_t speed);
void rr_track_forkward(uint8_t speed);
void rr_track_backward(uint8_t speed);

void drive(uint8_t left_power, uint8_t right_power, uint8_t directions);
void stop_tracks(void);

void display_tracks_info_header(void);
void display_tracks_info(void);
char *direction_itoa(unsigned short direction);

#endif /* TRACKS_DRIVER_H_ */
