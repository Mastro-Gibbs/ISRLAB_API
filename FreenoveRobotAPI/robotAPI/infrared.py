import RPi.GPIO as GPIO
from time import sleep

from workerthread import KillableThread


class Infrared:
    __IR_LEFT = 14
    __IR_MID = 15
    __IR_RIGHT = 23

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__IR_LEFT, GPIO.IN)
        GPIO.setup(self.__IR_MID, GPIO.IN)
        GPIO.setup(self.__IR_RIGHT, GPIO.IN)

        self.__left_status: bool  = False
        self.__mid_status: bool   = False
        self.__right_status: bool = False

        self.__discover = KillableThread(target=self.__detect, name='ir_discover')

    def virtual_destructor(self) -> str:
        return self.__discover.bury()

    def begin(self) -> None:
        if not self.__discover.is_alive():
            self.__discover.start()

    def __detect(self) -> None:
        self.__left_status  = False
        self.__mid_status   = False
        self.__right_status = False

        while True:
            self.__left_status  = self.__left
            self.__mid_status   = self.__mid
            self.__right_status = self.__right

            sleep(0.01)

    @property
    def __left(self) -> bool:
        return bool(GPIO.input(self.__IR_LEFT))

    @property
    def __mid(self) -> bool:
        return bool(GPIO.input(self.__IR_MID))

    @property
    def __right(self) -> bool:
        return bool(GPIO.input(self.__IR_RIGHT))

    @property
    def status(self) -> tuple:
        return int(self.__left_status), int(self.__mid_status), int(self.__right_status)


