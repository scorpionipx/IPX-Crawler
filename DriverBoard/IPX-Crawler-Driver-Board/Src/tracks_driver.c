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
#include "ili9341.h"

struct tracks_info{
	unsigned short fl_power;
	unsigned short fl_direction;

	unsigned short fr_power;
	unsigned short fr_direction;

	unsigned short rl_power;
	unsigned short rl_direction;

	unsigned short rr_power;
	unsigned short rr_direction;
}ipx_tracks;

void dummy(void)
{

}

void set_fl_track_dc(uint8_t duty_cycle)
{
	__HAL_TIM_SET_COMPARE(TRACKS_PWM_TIMER, FL_TRACK_TIMER_CHANNEL, duty_cycle);
	ipx_tracks.fl_power = duty_cycle;
}

void set_fr_track_dc(uint8_t duty_cycle)
{
	__HAL_TIM_SET_COMPARE(TRACKS_PWM_TIMER, FR_TRACK_TIMER_CHANNEL, duty_cycle);
	ipx_tracks.fr_power = duty_cycle;
}

void set_rl_track_dc(uint8_t duty_cycle)
{
	__HAL_TIM_SET_COMPARE(TRACKS_PWM_TIMER, RL_TRACK_TIMER_CHANNEL, duty_cycle);
	ipx_tracks.rl_power = duty_cycle;
}

void set_rr_track_dc(uint8_t duty_cycle)
{
	__HAL_TIM_SET_COMPARE(TRACKS_PWM_TIMER, RR_TRACK_TIMER_CHANNEL, duty_cycle);
	ipx_tracks.rr_power = duty_cycle;
}

void set_fl_track_direction_forward(void)
{
	HAL_GPIO_WritePin(FL_TRACK_DIRECTION_PORT, FL_TRACK_DIRECTION_BACKWARD_PIN, 0);
	HAL_GPIO_WritePin(FL_TRACK_DIRECTION_PORT, FL_TRACK_DIRECTION_FORWARD_PIN, 1);
	ipx_tracks.fl_direction = TRACK_DIRECTION_FORWARD;
}

void set_fl_track_direction_backward(void)
{
	HAL_GPIO_WritePin(FL_TRACK_DIRECTION_PORT, FL_TRACK_DIRECTION_FORWARD_PIN, 0);
	HAL_GPIO_WritePin(FL_TRACK_DIRECTION_PORT, FL_TRACK_DIRECTION_BACKWARD_PIN, 1);
	ipx_tracks.fl_direction = TRACK_DIRECTION_BACKWARD;
}

void set_fl_track_direction_none(void)
{
	HAL_GPIO_WritePin(FL_TRACK_DIRECTION_PORT, FL_TRACK_DIRECTION_FORWARD_PIN, 0);
	HAL_GPIO_WritePin(FL_TRACK_DIRECTION_PORT, FL_TRACK_DIRECTION_BACKWARD_PIN, 0);
	ipx_tracks.fl_direction = TRACK_DIRECTION_NONE;
}

void set_fr_track_direction_forward(void)
{
	HAL_GPIO_WritePin(FR_TRACK_DIRECTION_PORT, FR_TRACK_DIRECTION_BACKWARD_PIN, 0);
	HAL_GPIO_WritePin(FR_TRACK_DIRECTION_PORT, FR_TRACK_DIRECTION_FORWARD_PIN, 1);
	ipx_tracks.fr_direction = TRACK_DIRECTION_FORWARD;
}

void set_fr_track_direction_backward(void)
{
	HAL_GPIO_WritePin(FR_TRACK_DIRECTION_PORT, FR_TRACK_DIRECTION_FORWARD_PIN, 0);
	HAL_GPIO_WritePin(FR_TRACK_DIRECTION_PORT, FR_TRACK_DIRECTION_BACKWARD_PIN, 1);
	ipx_tracks.fr_direction = TRACK_DIRECTION_BACKWARD;
}

void set_fr_track_direction_none(void)
{
	HAL_GPIO_WritePin(FR_TRACK_DIRECTION_PORT, FR_TRACK_DIRECTION_FORWARD_PIN, 0);
	HAL_GPIO_WritePin(FR_TRACK_DIRECTION_PORT, FR_TRACK_DIRECTION_BACKWARD_PIN, 0);
	ipx_tracks.fr_direction = TRACK_DIRECTION_NONE;
}

void set_rl_track_direction_forward(void)
{
	HAL_GPIO_WritePin(RL_TRACK_DIRECTION_PORT, RL_TRACK_DIRECTION_BACKWARD_PIN, 0);
	HAL_GPIO_WritePin(RL_TRACK_DIRECTION_PORT, RL_TRACK_DIRECTION_FORWARD_PIN, 1);
	ipx_tracks.rl_direction = TRACK_DIRECTION_FORWARD;
}

void set_rl_track_direction_backward(void)
{
	HAL_GPIO_WritePin(RL_TRACK_DIRECTION_PORT, RL_TRACK_DIRECTION_FORWARD_PIN, 0);
	HAL_GPIO_WritePin(RL_TRACK_DIRECTION_PORT, RL_TRACK_DIRECTION_BACKWARD_PIN, 1);
	ipx_tracks.rl_direction = TRACK_DIRECTION_BACKWARD;
}

void set_rl_track_direction_none(void)
{
	HAL_GPIO_WritePin(RL_TRACK_DIRECTION_PORT, RL_TRACK_DIRECTION_FORWARD_PIN, 0);
	HAL_GPIO_WritePin(RL_TRACK_DIRECTION_PORT, RL_TRACK_DIRECTION_BACKWARD_PIN, 0);
	ipx_tracks.rl_direction = TRACK_DIRECTION_NONE;
}

void set_rr_track_direction_forward(void)
{
	HAL_GPIO_WritePin(RR_TRACK_DIRECTION_PORT, RR_TRACK_DIRECTION_BACKWARD_PIN, 0);
	HAL_GPIO_WritePin(RR_TRACK_DIRECTION_PORT, RR_TRACK_DIRECTION_FORWARD_PIN, 1);
	ipx_tracks.rr_direction = TRACK_DIRECTION_FORWARD;
}

void set_rr_track_direction_backward(void)
{
	HAL_GPIO_WritePin(RR_TRACK_DIRECTION_PORT, RR_TRACK_DIRECTION_FORWARD_PIN, 0);
	HAL_GPIO_WritePin(RR_TRACK_DIRECTION_PORT, RR_TRACK_DIRECTION_BACKWARD_PIN, 1);
	ipx_tracks.rr_direction = TRACK_DIRECTION_BACKWARD;
}

void set_rr_track_direction_none(void)
{
	HAL_GPIO_WritePin(RR_TRACK_DIRECTION_PORT, RR_TRACK_DIRECTION_FORWARD_PIN, 0);
	HAL_GPIO_WritePin(RR_TRACK_DIRECTION_PORT, RR_TRACK_DIRECTION_BACKWARD_PIN, 0);
	ipx_tracks.rr_direction = TRACK_DIRECTION_NONE;
}

void fl_track_forward(uint8_t speed)
{
	set_fl_track_direction_forward();
	set_fl_track_dc(speed);
}

void fl_track_backward(uint8_t speed)
{
	set_fl_track_direction_backward();
	set_fl_track_dc(speed);
}

void fr_track_forward(uint8_t speed)
{
	set_fr_track_direction_forward();
	set_fr_track_dc(speed);
}

void fr_track_backward(uint8_t speed)
{
	set_fr_track_direction_backward();
	set_fr_track_dc(speed);
}


void rl_track_forward(uint8_t speed)
{
	set_rl_track_direction_forward();
	set_rl_track_dc(speed);
}

void rl_track_backward(uint8_t speed)
{
	set_rl_track_direction_backward();
	set_rl_track_dc(speed);
}

void rr_track_forward(uint8_t speed)
{
	set_rr_track_direction_forward();
	set_rr_track_dc(speed);
}

void rr_track_backward(uint8_t speed)
{
	set_rr_track_direction_backward();
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

	ipx_tracks.fl_direction = TRACK_DIRECTION_NONE;
	ipx_tracks.fr_direction = TRACK_DIRECTION_NONE;
	ipx_tracks.rl_direction = TRACK_DIRECTION_NONE;
	ipx_tracks.rr_direction = TRACK_DIRECTION_NONE;

	set_fl_track_dc(0);
	set_fr_track_dc(0);
	set_rl_track_dc(0);
	set_rr_track_dc(0);
}

void set_fl_track_direction(unsigned short direction)
{
	switch(direction)
	{
		case TRACK_DIRECTION_NONE:
		{
			set_fl_track_direction_none();
			break;
		}
		case TRACK_DIRECTION_FORWARD:
		{
			set_fl_track_direction_forward();
			break;
		}
		case TRACK_DIRECTION_BACKWARD:
		{
			set_fl_track_direction_backward();
			break;
		}
	}
}

void set_fr_track_direction(unsigned short direction)
{
	switch(direction)
	{
		case TRACK_DIRECTION_NONE:
		{
			set_fr_track_direction_none();
			break;
		}
		case TRACK_DIRECTION_FORWARD:
		{
			set_fr_track_direction_forward();
			break;
		}
		case TRACK_DIRECTION_BACKWARD:
		{
			set_fr_track_direction_backward();
			break;
		}
	}
}

void set_rl_track_direction(unsigned short direction)
{
	switch(direction)
	{
		case TRACK_DIRECTION_NONE:
		{
			set_rl_track_direction_none();
			break;
		}
		case TRACK_DIRECTION_FORWARD:
		{
			set_rl_track_direction_forward();
			break;
		}
		case TRACK_DIRECTION_BACKWARD:
		{
			set_rl_track_direction_backward();
			break;
		}
	}
}

void set_rr_track_direction(unsigned short direction)
{
	switch(direction)
	{
		case TRACK_DIRECTION_NONE:
		{
			set_rr_track_direction_none();
			break;
		}
		case TRACK_DIRECTION_FORWARD:
		{
			set_rr_track_direction_forward();
			break;
		}
		case TRACK_DIRECTION_BACKWARD:
		{
			set_rr_track_direction_backward();
			break;
		}
	}
}

void set_track_direction(unsigned short track, unsigned short direction)
{
	switch(track)
	{
		case FL_TRACK:
		{
			set_fl_track_direction(direction);
			break;
		}
		case FR_TRACK:
		{
			set_fr_track_direction(direction);
			break;
		}
		case RL_TRACK:
		{
			set_rl_track_direction(direction);
			break;
		}
		case RR_TRACK:
		{
			set_rr_track_direction(direction);
			break;
		}
	}
}

void joystick_drive(signed short x, signed short y)
{
	if(x >=0 && y >= 100)
	{

	}

}

void drive(uint8_t left_power, uint8_t right_power, uint8_t directions)
{
	set_fl_track_dc(left_power);
	set_rl_track_dc(left_power);

	set_fr_track_dc(right_power);
	set_rr_track_dc(right_power);

	uint8_t left_direction = (directions >> 2) & 3;
	uint8_t right_direction = directions & 3;

	set_fl_track_direction(left_direction);
	set_fr_track_direction(right_direction);
	set_rl_track_direction(left_direction);
	set_rr_track_direction(right_direction);
}

void init_tracks_control(void)
{
	stop_tracks();
}

void display_tracks_info_header(void)
{
	int x = 150;
	int y = 32;
	int spacing = 8;

	print_str(x, y, 1, Green, Black, "  TRACKS INFO");
	print_str(x, y + spacing, 1, Green, Black, "   POW || DIR");
	print_str(x, y + spacing * 2, 1, Green, Black, "FL N/A || N/A");
	print_str(x, y + spacing * 3, 1, Green, Black, "FR N/A || N/A");
	print_str(x, y + spacing * 4, 1, Green, Black, "RL N/A || N/A");
	print_str(x, y + spacing * 5, 1, Green, Black, "RR N/A || N/A");
}

void display_tracks_info(void)
{
	int x = 150;
	int y = 32;
	int spacing = 8;

	print_str(x + 6 * 3, y + spacing * 2, 1, Green, Black, Itoa(ipx_tracks.fl_power, 10, 3));
	print_str(x + 6 * 3, y + spacing * 3, 1, Green, Black, Itoa(ipx_tracks.fr_power, 10, 3));
	print_str(x + 6 * 3, y + spacing * 4, 1, Green, Black, Itoa(ipx_tracks.rl_power, 10, 3));
	print_str(x + 6 * 3, y + spacing * 5, 1, Green, Black, Itoa(ipx_tracks.rr_power, 10, 3));

	print_str(x + 6 * 10, y + spacing * 2, 1, Green, Black, direction_itoa(ipx_tracks.fl_direction));
	print_str(x + 6 * 10, y + spacing * 3, 1, Green, Black, direction_itoa(ipx_tracks.fr_direction));
	print_str(x + 6 * 10, y + spacing * 4, 1, Green, Black, direction_itoa(ipx_tracks.rl_direction));
	print_str(x + 6 * 10, y + spacing * 5, 1, Green, Black, direction_itoa(ipx_tracks.rr_direction));
}

char *direction_itoa(unsigned short direction)
{
	switch(direction)
	{
		case 0:
		{
			return "N/A";
		}
		case 1:
		{
			return "FWD";
		}
		case 2:
		{
			return "BWD";
		}
		default:
		{
			return "ERR";
		}
	}
}
