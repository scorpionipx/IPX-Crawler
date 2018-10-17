/**
  ******************************************************************************
  * File Name          : main.c
  * Description        : Main program body
  ******************************************************************************
  *
  * COPYRIGHT(c) 2018 STMicroelectronics
  *
  * Redistribution and use in source and binary forms, with or without modification,
  * are permitted provided that the following conditions are met:
  *   1. Redistributions of source code must retain the above copyright notice,
  *      this list of conditions and the following disclaimer.
  *   2. Redistributions in binary form must reproduce the above copyright notice,
  *      this list of conditions and the following disclaimer in the documentation
  *      and/or other materials provided with the distribution.
  *   3. Neither the name of STMicroelectronics nor the names of its contributors
  *      may be used to endorse or promote products derived from this software
  *      without specific prior written permission.
  *
  * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
  * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
  * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
  * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
  * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
  * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
  * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
  * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
  * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
  * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
  *
  ******************************************************************************
  */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "stm32f4xx_hal.h"
#include "spi.h"
#include "tim.h"
#include "gpio.h"

/* USER CODE BEGIN Includes */
#include "ili9341.h"
#include "tracks_driver.h"
#include "headlights_driver.h"
/* USER CODE END Includes */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */
/* Private variables ---------------------------------------------------------*/
uint8_t spi_buffer = 0x00;
struct ipx_spi_command {
  unsigned short id;
  unsigned short data_0;
  unsigned short data_1;
  unsigned short data_2;
  unsigned short data_3;
} ipx_command;
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
void Error_Handler(void);

/* USER CODE BEGIN PFP */
/* Private function prototypes -----------------------------------------------*/

/* USER CODE END PFP */

/* USER CODE BEGIN 0 */
void spi_data_handler(uint8_t spi_buffer);
void display_command_header(void);
void display_command(void);
void execute_command(struct ipx_spi_command command);

unsigned short pos = 0;
/* USER CODE END 0 */

int main(void)
{

  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration----------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* Configure the system clock */
  SystemClock_Config();

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_SPI4_Init();
  MX_SPI5_Init();
  MX_TIM4_Init();

  /* USER CODE BEGIN 2 */

  HAL_GPIO_WritePin(GPIOG, GPIO_PIN_13, SET);
  HAL_SPI_Receive_IT(&hspi4, &spi_buffer, 1);

  TFT_init();
  TFT_on_off(0x29);
  TFT_fill(Black);

  HEADLIGHT_LEFT_ON;
  HEADLIGHT_RIGHT_ON;

  print_str(60, 0, 1, Green, Black, "ScorpionIPX Crawler Driver Board v0.0.1");

  display_command_header();

  init_tracks_control();
  display_tracks_info_header();
  display_tracks_info();

  HAL_TIM_Base_Start(&htim4);
  HAL_TIM_PWM_Start(&htim4, TIM_CHANNEL_1);
  HAL_TIM_PWM_Start(&htim4, TIM_CHANNEL_2);
  HAL_TIM_PWM_Start(&htim4, TIM_CHANNEL_3);
  HAL_TIM_PWM_Start(&htim4, TIM_CHANNEL_4);
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
  /* USER CODE END WHILE */

  /* USER CODE BEGIN 3 */

  }
  /* USER CODE END 3 */

}

/** System Clock Configuration
*/
void SystemClock_Config(void)
{

  RCC_OscInitTypeDef RCC_OscInitStruct;
  RCC_ClkInitTypeDef RCC_ClkInitStruct;

    /**Configure the main internal regulator output voltage 
    */
  __HAL_RCC_PWR_CLK_ENABLE();

  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

    /**Initializes the CPU, AHB and APB busses clocks 
    */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLM = 4;
  RCC_OscInitStruct.PLL.PLLN = 180;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = 7;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

    /**Activate the Over-Drive mode 
    */
  if (HAL_PWREx_EnableOverDrive() != HAL_OK)
  {
    Error_Handler();
  }

    /**Initializes the CPU, AHB and APB busses clocks 
    */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV4;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_5) != HAL_OK)
  {
    Error_Handler();
  }

    /**Configure the Systick interrupt time 
    */
  HAL_SYSTICK_Config(HAL_RCC_GetHCLKFreq()/1000);

    /**Configure the Systick 
    */
  HAL_SYSTICK_CLKSourceConfig(SYSTICK_CLKSOURCE_HCLK);

  /* SysTick_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(SysTick_IRQn, 0, 0);
}

/* USER CODE BEGIN 4 */
void HAL_SPI_RxCpltCallback(SPI_HandleTypeDef *hspi)
{
	HAL_GPIO_TogglePin(GPIOG, GPIO_PIN_14);
	HAL_GPIO_TogglePin(GPIOG, GPIO_PIN_13);
	HAL_SPI_Receive_IT(&hspi4, &spi_buffer, 1);
	switch(pos)
	{
	case 0:
	{
		ipx_command.id = spi_buffer;
		break;
	}
	case 1:
	{
		ipx_command.data_0 = spi_buffer;
		break;
	}
	case 2:
	{
		ipx_command.data_1 = spi_buffer;
		break;
	}
	case 3:
	{
		ipx_command.data_2 = spi_buffer;
		break;
	}
	case 4:
	{
		ipx_command.data_3 = spi_buffer;
		display_command();
		execute_command(ipx_command);
		break;
	}
	default:
		pos = 0;
		break;
	}

	pos ++;
	if(pos > 4)
	{
		pos = 0;
	}
}

void spi_data_handler(uint8_t spi_buffer)
{
	  if(spi_buffer == 0x0f)
	  {
		  HAL_GPIO_WritePin(GPIOG, GPIO_PIN_13, GPIO_PIN_SET);
		  HAL_GPIO_WritePin(GPIOG, GPIO_PIN_14, GPIO_PIN_RESET);
	  }
	  else if (spi_buffer == 0xf0)
	  {
		  HAL_GPIO_WritePin(GPIOG, GPIO_PIN_13, GPIO_PIN_RESET);
		  HAL_GPIO_WritePin(GPIOG, GPIO_PIN_14, GPIO_PIN_RESET);
	  }
	  else
	  {
		  // HAL_GPIO_WritePin(GPIOG, GPIO_PIN_14, GPIO_PIN_SET);
	  }
}

void display_command_header(void)
{
	int x = 10;
	int y = 32;
	int spacing = 8;

	print_str(x, y, 1, Green, Black, "IPX COMMAND");
	print_str(x, y + spacing, 1, Green, Black, "ID: N/A");
	print_str(x, y + spacing * 2, 1, Green, Black, "DATA_0: N/A");
	print_str(x, y + spacing * 3, 1, Green, Black, "DATA_1: N/A");
	print_str(x, y + spacing * 4, 1, Green, Black, "DATA_2: N/A");
	print_str(x, y + spacing * 5, 1, Green, Black, "DATA_3: N/A");
}
void display_command(void)
{
	int x = 10;
	int y = 32;
	int spacing = 8;

	print_str(x + 6 * 4, y + spacing, 1, Green, Black, Itoa(ipx_command.id, 10, 3));
	print_str(x + 6 * 8, y + spacing * 2, 1, Green, Black, Itoa(ipx_command.data_0, 10, 3));
	print_str(x + 6 * 8, y + spacing * 3, 1, Green, Black, Itoa(ipx_command.data_1, 10, 3));
	print_str(x + 6 * 8, y + spacing * 4, 1, Green, Black, Itoa(ipx_command.data_2, 10, 3));
	print_str(x + 6 * 8, y + spacing * 5, 1, Green, Black, Itoa(ipx_command.data_3, 10, 3));
}

void execute_command(struct ipx_spi_command command)
{
	switch(command.id)
	{
		case 1:
		{
			set_fl_track_dc(command.data_0);
			set_fr_track_dc(command.data_1);
			set_rl_track_dc(command.data_2);
			set_rr_track_dc(command.data_3);
			display_tracks_info();
			break;
		}

		case 2:
		{
			set_fl_track_direction(command.data_0);
			set_fr_track_direction(command.data_1);
			set_rl_track_direction(command.data_2);
			set_rr_track_direction(command.data_3);
			display_tracks_info();
			break;
		}

		case 3:
		{
			if(command.data_0)
			{
				HEADLIGHT_LEFT_ON;
			}
			else
			{
				HEADLIGHT_LEFT_OFF;
			}
			if(command.data_1)
			{
				HEADLIGHT_RIGHT_ON;
			}
			else
			{
				HEADLIGHT_RIGHT_OFF;
			}

			break;
		}

		default:
		{
			break;
		}
	}
}
/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @param  None
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler */
  /* User can add his own implementation to report the HAL error return state */
  while(1) 
  {
  }
  /* USER CODE END Error_Handler */ 
}

#ifdef USE_FULL_ASSERT

/**
   * @brief Reports the name of the source file and the source line number
   * where the assert_param error has occurred.
   * @param file: pointer to the source file name
   * @param line: assert_param error line source number
   * @retval None
   */
void assert_failed(uint8_t* file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
    ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */

}

#endif

/**
  * @}
  */ 

/**
  * @}
*/ 

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
