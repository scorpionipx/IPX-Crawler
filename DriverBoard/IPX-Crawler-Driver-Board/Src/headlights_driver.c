/*
 * headlights_driver.c
 *
 *  Created on: Oct 17, 2018
 *      Author: ScorpionIPX
 */

#include "headlights_driver.h"

void light_control_check(void)
{
	  HEADLIGHT_LEFT_ON;
	  HEADLIGHT_RIGHT_ON;
	  HAL_Delay(500);
	  HEADLIGHT_LEFT_OFF;
	  HEADLIGHT_RIGHT_OFF;
	  HAL_Delay(500);
	  for(int short i = 0; i < 15; i++)
	  {
		  HEADLIGHT_LEFT_ON;
		  HEADLIGHT_RIGHT_OFF;
		  HAL_Delay(50);
		  HEADLIGHT_LEFT_OFF;
		  HEADLIGHT_RIGHT_ON;
		  HAL_Delay(50);
	  }
	  HEADLIGHT_LEFT_ON;
	  HEADLIGHT_RIGHT_ON;
	  HAL_Delay(500);
	  HEADLIGHT_LEFT_OFF;
	  HEADLIGHT_RIGHT_OFF;
}
