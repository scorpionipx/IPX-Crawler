import pygame

pygame.init()
pygame.joystick.init()

joystick_count = pygame.joystick.get_count()
if joystick_count > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    axes = joystick.get_numaxes()

    number_of_buttons = joystick.get_numbuttons()
    button_pressed = [False] * number_of_buttons


while True:
    pygame.event.pump()
    # z = int(self.joystick.get_axis(4) * 100)
    # LOGGER.info("Z axis: {}".format(z))
    for button_index in range(number_of_buttons):
        if joystick.get_button(button_index):
            button_pressed[button_index] = True
            print("Button {} pressed".format(button_index))
