/*
 * ili9341.c
 *
 *  Created on: 21 oct. 2016
 *      Author: uidg9626
 */
#include "main.h"
#include "spi.h"
#include "ILI9341.h"

static uint16_t MAXX = X_max;
static uint16_t MAXY = Y_max;

void TFT_init()
{
  TFT_write(ILI9341_RESET, CMD);
  HAL_Delay(60);

  TFT_write(ILI9341_POWERA, CMD);
  TFT_write(0x39, DAT);
  TFT_write(0x2C, DAT);
  TFT_write(0x00, DAT);
  TFT_write(0x34, DAT);
  TFT_write(0x02, DAT);

  TFT_write(ILI9341_POWERB, CMD);
  TFT_write(0x00, DAT);
  TFT_write(0xC1, DAT);
  TFT_write(0x30, DAT);

  TFT_write(ILI9341_DTCA, CMD);
  TFT_write(0x85, DAT);
  TFT_write(0x00, DAT);
  TFT_write(0x78, DAT);

  TFT_write(ILI9341_DTCB, CMD);
  TFT_write(0x00, DAT);
  TFT_write(0x00, DAT);

  TFT_write(ILI9341_POWER_SEQ, CMD);
  TFT_write(0x64, DAT);
  TFT_write(0x03, DAT);
  TFT_write(0x12, DAT);
  TFT_write(0x81, DAT);

  TFT_write(ILI9341_PRC, CMD);
  TFT_write(0x20, DAT);

  TFT_write(ILI9341_POWER1, CMD);
  TFT_write(0x23, DAT);

  TFT_write(ILI9341_POWER2, CMD);
  TFT_write(0x10, DAT);

  TFT_write(ILI9341_VCOM1, CMD);
  TFT_write(0x3E, DAT);
  TFT_write(0x28, DAT);

  TFT_write(ILI9341_VCOM2, CMD);
  TFT_write(0x86, DAT);

  TFT_write(ILI9341_MAC, CMD);
  TFT_write(0x48, DAT);

  TFT_write(ILI9341_PIXEL_FORMAT, CMD);
  TFT_write(0x55, DAT);

  TFT_write(ILI9341_FRC, CMD);
  TFT_write(0x00, DAT);
  TFT_write(0x18, DAT);

  TFT_write(ILI9341_DFC, CMD);
  TFT_write(0x08, DAT);
  TFT_write(0x82, DAT);
  TFT_write(0x27, DAT);

  TFT_write(ILI9341_3GAMMA_EN, CMD);
  TFT_write(0x00, DAT);

  TFT_write(ILI9341_COLUMN_ADDR, CMD);
  TFT_write(0x00, DAT);
  TFT_write(0x00, DAT);
  TFT_write(0x00, DAT);
  TFT_write(0xEF, DAT);

  TFT_write(ILI9341_PAGE_ADDR, CMD);
  TFT_write(0x00, DAT);
  TFT_write(0x00, DAT);
  TFT_write(0x01, DAT);
  TFT_write(0x3F, DAT);

  TFT_write(ILI9341_GAMMA, CMD);
  TFT_write(0x01, DAT);

  TFT_write(ILI9341_PGAMMA, CMD);
  TFT_write(0x0F, DAT);
  TFT_write(0x31, DAT);
  TFT_write(0x2B, DAT);
  TFT_write(0x0C, DAT);
  TFT_write(0x0E, DAT);
  TFT_write(0x08, DAT);
  TFT_write(0x4E, DAT);
  TFT_write(0xF1, DAT);
  TFT_write(0x37, DAT);
  TFT_write(0x07, DAT);
  TFT_write(0x10, DAT);
  TFT_write(0x03, DAT);
  TFT_write(0x0E, DAT);
  TFT_write(0x09, DAT);
  TFT_write(0x00, DAT);

  TFT_write(ILI9341_NGAMMA, CMD);
  TFT_write(0x00, DAT);
  TFT_write(0x0E, DAT);
  TFT_write(0x14, DAT);
  TFT_write(0x03, DAT);
  TFT_write(0x11, DAT);
  TFT_write(0x07, DAT);
  TFT_write(0x31, DAT);
  TFT_write(0xC1, DAT);
  TFT_write(0x48, DAT);
  TFT_write(0x08, DAT);
  TFT_write(0x0F, DAT);
  TFT_write(0x0C, DAT);
  TFT_write(0x31, DAT);
  TFT_write(0x36, DAT);
  TFT_write(0x0F, DAT);

  TFT_write(ILI9341_SLEEP_OUT, CMD);
  HAL_Delay(100);

  TFT_on_off(ON);
  TFT_write(ILI9341_GRAM, CMD);

  TFT_set_rotation(LANDSCAPE_2);
}

void TFT_write(uint8_t value, uint8_t mode)
{
  HAL_GPIO_WritePin(WRX_DCX_GPIO_Port, WRX_DCX_Pin, mode);
  HAL_GPIO_WritePin(CSX_GPIO_Port, CSX_Pin, LOW);
  HAL_SPI_Transmit(&hspi5, &value, 1, 1);
  HAL_GPIO_WritePin(CSX_GPIO_Port, CSX_Pin, HIGH);
}

void TFT_write_word(uint16_t value, uint8_t mode)
{
  uint8_t hb = 0x00;
  uint8_t lb = 0x00;

  lb = (value & 0x00FF);
  hb = (value >> 0x08);

  HAL_GPIO_WritePin(WRX_DCX_GPIO_Port, WRX_DCX_Pin, mode);
  HAL_GPIO_WritePin(CSX_GPIO_Port, CSX_Pin, LOW);
  HAL_SPI_Transmit(&hspi5, &hb, 1, 1);
  HAL_SPI_Transmit(&hspi5, &lb, 1, 1);
  HAL_GPIO_WritePin(CSX_GPIO_Port, CSX_Pin, HIGH);
}

void TFT_on_off(uint8_t mode)
{
  switch (mode)
  {
    case ON:
    {
      TFT_write(ILI9341_DISPLAY_ON, CMD);
      break;
    }
    case OFF:
    {
      TFT_write(ILI9341_DISPLAY_OFF, CMD);
      break;
    }
  }
}

void TFT_set_rotation(uint8_t value)
{
  TFT_write(ILI9341_MAC, CMD);

  switch (value)
  {
    case PORTRAIT_1:
    {
      TFT_write(0x58, DAT);
      break;
    }
    case PORTRAIT_2:
    {
      TFT_write(0x88, DAT);
      break;
    }
    case LANDSCAPE_1:
    {
      TFT_write(0x28, DAT);
      break;
    }
    case LANDSCAPE_2:
    {
      TFT_write(0xE8, DAT);
      break;
    }
  }

  if ((value == PORTRAIT_1) || (value == PORTRAIT_2))
  {
    MAXX = X_max;
    MAXY = Y_max;
  }

  if ((value == LANDSCAPE_1) || (value == LANDSCAPE_2))
  {
    MAXX = Y_max;
    MAXY = X_max;
  }
}

void TFT_set_display_window(uint16_t x_pos1, uint16_t y_pos1, uint16_t x_pos2, uint16_t y_pos2)
{
  TFT_write(ILI9341_COLUMN_ADDR, CMD);
  TFT_write_word(x_pos1, DAT);
  TFT_write_word(x_pos2, DAT);

  TFT_write(ILI9341_PAGE_ADDR, CMD);
  TFT_write_word(y_pos1, DAT);
  TFT_write_word(y_pos2, DAT);

  TFT_write(ILI9341_GRAM, CMD);
}

void TFT_fill(uint16_t colour)
{
  unsigned long index = pixels;

  TFT_set_display_window(0, 0, (MAXX - 1), (MAXY - 1));

  while (index)
  {
    TFT_write_word(colour, DAT);
    index--;
  };
}

void TFT_fill_area(int16_t x1, int16_t y1, int16_t x2, int16_t y2, uint16_t colour)
{
  unsigned long index = 0x00000000;

  if (x1 > x2)
  {
    swap(&x1, &x2);
  }
  if (y1 > y2)
  {
    swap(&y1, &y2);
  }

  index = (x2 - x1);
  index *= (y2 - y1);

  TFT_set_display_window(x1, y1, (x2 - 1), (y2 - 1));

  while (index)
  {
    TFT_write_word(colour, DAT);
    index--;
  };
}

void swap(int16_t *a, int16_t *b)
{
  int16_t temp = 0x0000;

  temp = *b;
  *b = *a;
  *a = temp;
}

void Draw_Pixel(uint16_t x_pos, uint16_t y_pos, uint16_t colour)
{
  TFT_set_display_window(x_pos, y_pos, x_pos, y_pos);
  TFT_write_word(colour, DAT);
}

void Draw_Point(uint16_t x_pos, uint16_t y_pos, uint8_t pen_width, uint16_t colour)
{
  Draw_Circle(x_pos, y_pos, pen_width, YES, colour);
}

void Draw_Line(int16_t x1, int16_t y1, int16_t x2, int16_t y2, uint16_t colour)
{
  int16_t dx = 0x0000;
  int16_t dy = 0x0000;
  int16_t stepx = 0x0000;
  int16_t stepy = 0x0000;
  int16_t fraction = 0x0000;

  dy = (y2 - y1);
  dx = (x2 - x1);

  if (dy < 0)
  {
    dy = -dy;
    stepy = -1;
  }
  else
  {
    stepy = 1;
  }

  if (dx < 0)
  {
    dx = -dx;
    stepx = -1;
  }
  else
  {
    stepx = 1;
  }

  dx <<= 0x01;
  dy <<= 0x01;

  Draw_Pixel(x1, y1, colour);

  if (dx > dy)
  {
    fraction = (dy - (dx >> 1));
    while (x1 != x2)
    {
      if (fraction >= 0)
      {
        y1 += stepy;
        fraction -= dx;
      }
      x1 += stepx;
      fraction += dy;

      Draw_Pixel(x1, y1, colour);
    }
  }
  else
  {
    fraction = (dx - (dy >> 1));

    while (y1 != y2)
    {
      if (fraction >= 0)
      {
        x1 += stepx;
        fraction -= dy;
      }
      y1 += stepy;
      fraction += dx;
      Draw_Pixel(x1, y1, colour);
    }
  }
}

void Draw_V_Line(int16_t x1, int16_t y1, int16_t y2, unsigned colour)
{

  if (y1 > y2)
  {
    swap(&y1, &y2);
  }

  while (y2 > (y1 - 1))
  {
    Draw_Pixel(x1, y2, colour);
    y2--;
  }
}

void Draw_H_Line(int16_t x1, int16_t x2, int16_t y1, unsigned colour)
{
  if (x1 > x2)
  {
    swap(&x1, &x2);
  }

  while (x2 > (x1 - 1))
  {
    Draw_Pixel(x2, y1, colour);
    x2--;
  }
}

void Draw_Rectangle(int16_t x1, int16_t y1, int16_t x2, int16_t y2, uint8_t fill, uint8_t type, uint16_t colour, uint16_t back_colour)
{
  int16_t i = 0x0000;
  int16_t xmin = 0x0000;
  int16_t xmax = 0x0000;
  int16_t ymin = 0x0000;
  int16_t ymax = 0x0000;

  switch (fill)
  {
    case YES:
    {
      if (x1 < x2)
      {
        xmin = x1;
        xmax = x2;
      }
      else
      {
        xmin = x2;
        xmax = x1;
      }

      if (y1 < y2)
      {
        ymin = y1;
        ymax = y2;
      }
      else
      {
        ymin = y2;
        ymax = y1;
      }

      for (; xmin <= xmax; ++xmin)
      {
        for (i = ymin; i <= ymax; ++i)
        {
          Draw_Pixel(xmin, i, colour);
        }
      }

      break;
    }
    default:
    {
      Draw_V_Line(x1, y1, y2, colour);
      Draw_V_Line(x2, y1, y2, colour);
      Draw_H_Line(x1, x2, y1, colour);
      Draw_H_Line(x1, x2, y2, colour);
      break;
    }
  }

  if (type != SQUARE)
  {
    Draw_Pixel(x1, y1, back_colour);
    Draw_Pixel(x1, y2, back_colour);
    Draw_Pixel(x2, y1, back_colour);
    Draw_Pixel(x2, y2, back_colour);
  }
}

void Draw_Circle(int16_t xc, int16_t yc, int16_t radius, uint8_t fill, uint16_t colour)
{
  int16_t a = 0x0000;
  int16_t b = 0x0000;
  int16_t p = 0x0000;

  b = radius;
  p = (1 - b);

  do
  {
    switch (fill)
    {
      case YES:
      {
        Draw_Line((xc - a), (yc + b), (xc + a), (yc + b), colour);
        Draw_Line((xc - a), (yc - b), (xc + a), (yc - b), colour);
        Draw_Line((xc - b), (yc + a), (xc + b), (yc + a), colour);
        Draw_Line((xc - b), (yc - a), (xc + b), (yc - a), colour);
        break;
      }
      default:
      {
        Draw_Pixel((xc + a), (yc + b), colour);
        Draw_Pixel((xc + b), (yc + a), colour);
        Draw_Pixel((xc - a), (yc + b), colour);
        Draw_Pixel((xc - b), (yc + a), colour);
        Draw_Pixel((xc + b), (yc - a), colour);
        Draw_Pixel((xc + a), (yc - b), colour);
        Draw_Pixel((xc - a), (yc - b), colour);
        Draw_Pixel((xc - b), (yc - a), colour);
        break;
      }
    }

    if (p < 0)
    {
      p += (0x03 + (0x02 * a++));
    }
    else
    {
      p += (0x05 + (0x02 * ((a++) - (b--))));
    }
  } while (a <= b);
}

void Draw_Font_Pixel(uint16_t x_pos, uint16_t y_pos, uint16_t colour, uint8_t pixel_size)
{
  uint8_t i = (pixel_size * pixel_size);

  TFT_set_display_window(x_pos, y_pos, (x_pos + pixel_size - 1), (y_pos + pixel_size - 1));

  while (i > 0)
  {
    TFT_write_word(colour, DAT);
    i--;
  }
}

void print_char(uint16_t x_pos, uint16_t y_pos, uint8_t font_size, uint16_t colour, uint16_t back_colour, uint8_t ch)
{
  uint8_t i = 0x00;
  uint8_t j = 0x00;
  uint8_t value = 0x00;

  if (font_size <= 0)
  {
    font_size = 1;
  }

  if (x_pos < font_size)
  {
    x_pos = font_size;
  }

  for (i = 0x00; i < 0x05; i++)
  {
    for (j = 0x00; j < 0x08; j++)
    {
      value = 0x0000;
      value = ((font[((uint8_t) ch) - 0x20][i]));

      if (((value >> j) & 0x01) != 0x00)
      {
        Draw_Font_Pixel(x_pos, y_pos, colour, font_size);
      }
      else
      {
        Draw_Font_Pixel(x_pos, y_pos, back_colour, font_size);
      }

      y_pos += font_size;
    }

    y_pos -= (font_size << 0x03);
    x_pos += font_size;
  }
}

void print_str(uint16_t x_pos, uint16_t y_pos, uint8_t font_size, uint16_t colour, uint16_t back_colour, uint8_t *ch)
{
  while (*ch != '\0')
  {
    print_char(x_pos, y_pos, font_size, colour, back_colour, *ch++);
    x_pos += (font_size * 0x06);
  }
}

char *Itoa(int32_t Value, uint8_t Base, uint8_t Digits)
{
  static char Text_Buff[32];
  static char Sir[16] = "0123456789ABCDEF";
  char *Text_Address;
  unsigned char idx = 30;
  unsigned char numbers = 0;
  Text_Buff[31] = '\0';
  if (Value > 0)
  {
    while (Value > 0)
    {
      Text_Buff[idx] = Sir[Value % Base];
      Value = Value / Base;
      idx--;
      numbers++;
    }
    while ((Digits - numbers) > 0)
    {
      Text_Buff[idx] = ' ';
      idx--;
      Digits--;
    }
    Text_Address = &Text_Buff[idx + 1];
  }
  else
  {
    if (Value < 0)
    {
      while (Value < 0)
      {
        Text_Buff[idx] = Sir[((~Value) + 1) % Base];
        Value = Value / Base;
        idx--;
        numbers++;
      }
      if (Base == 10)
      {
        Text_Buff[idx] = '-';
        while ((Digits - (numbers + 1)) > 0)
        {
          idx--;
          Text_Buff[idx] = ' ';
          Digits--;
        }
        Text_Address = &Text_Buff[idx];
      }
      else
      {
        while ((Digits - numbers ) > 0)
        {
          Text_Buff[idx] = ' ';
          idx--;
          Digits--;
        }
        Text_Address = &Text_Buff[idx+1];
      }


    }
    else
    {
      Text_Buff[idx] = '0';
      while (--Digits)
      {
        idx--;
        Text_Buff[idx] = ' ';
      }
      Text_Address = &Text_Buff[idx];
    }
  }
  return Text_Address;
}

