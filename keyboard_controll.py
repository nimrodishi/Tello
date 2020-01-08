import pygame
from tello import Tello
from typing import Tuple, Optional
import logging
from CameraStream import CameraStream
import cv2
import numpy as np
from utils import generate_logger
from mock import MagicMock


class KeyboardControl:
    """
    controlling the drone via keyboard
    """

    LOGGER = generate_logger("KeyboardController")

    def __init__(self, drone: Tello, control_window_size: Tuple[int, int] = (1280, 720),
                 camera: Optional[CameraStream] = None):
        self.drone = drone
        self.move_amount = 20
        self.rotate_amount = 30
        self.camera = camera
        self.control_window_size = control_window_size
        pygame.init()
        self.screen = pygame.display.set_mode(self.control_window_size)

    def __repr__(self):
        return f"<{self.__class__.__name__} for {self.drone}>"

    def pass_control(self):
        self.LOGGER.debug("Passing control to keyboard, press 'h' for help")
        pygame.display.set_caption("DJI Tello Control Window")
        running = True
        while running:
            if self.camera:
                ret, frame = self.camera.get_frames()

                self.screen.fill([0, 0, 0])
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = np.rot90(frame)
                frame = pygame.surfarray.make_surface(frame)
                self.screen.blit(frame, (0, 0))
                pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.drone.move_right(self.move_amount)
                        self.LOGGER.debug(f"moving {self.move_amount} to the right")
                    elif event.key == pygame.K_LEFT:
                        self.drone.move_left(self.move_amount)
                        self.LOGGER.debug(f"moving {self.move_amount} to the left")
                    elif event.key == pygame.K_UP:
                        self.drone.move_forward(self.move_amount)
                        self.LOGGER.debug(f"moving {self.move_amount} forwards")
                    elif event.key == pygame.K_DOWN:
                        self.drone.move_back(self.move_amount)
                        self.LOGGER.debug(f"moving {self.move_amount} backwards")
                    elif event.key == pygame.K_q:
                        self.drone.rotate_counter_clockwise(self.rotate_amount)
                        self.LOGGER.debug(f"rotating {self.rotate_amount} counter-clockwise")
                    elif event.key == pygame.K_e:
                        self.drone.rotate_clockwise(self.rotate_amount)
                        self.LOGGER.debug(f"rotating {self.rotate_amount} clockwise")
                    elif event.key == pygame.K_LCTRL:
                        self.drone.move_down(self.move_amount)
                        self.LOGGER.debug(f"moving {self.move_amount} down")
                    elif event.key == pygame.K_LALT:
                        self.drone.move_up(self.move_amount)
                        self.LOGGER.debug(f"moving {self.move_amount} up")
                    elif event.key == pygame.K_ESCAPE:
                        self.LOGGER.debug("Returning control")
                        running = False
                    elif event.key == pygame.K_h:
                        print(
                            "Drone is being controlled by keyboard;\n"
                            "\t- Arrow Up:      move forward\n"
                            "\t- Arrow Down:    move forward\n"
                            "\t- Arrow Left:    move forward\n"
                            "\t- Arrow Right:   move forward\n"
                            "\t- Left Ctrl:     move forward\n"
                            "\t- Left Alt:      move forward\n"
                            "\t- q:             rotate counter clockwise\n"
                            "\t- e:             rotate clockwise\n"
                        )


if __name__ == "__main__":
    from mock import MagicMock

    drone = MagicMock()
    kc = KeyboardControl(drone)
    KeyboardControl.LOGGER.setLevel(logging.DEBUG)
    KeyboardControl(drone).pass_control()
