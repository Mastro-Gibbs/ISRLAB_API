from time import time, sleep
import RPi.GPIO as GPIO


class Ultrasonic:

    def __init__(self, echo_pin: int, trigger_pin: int):
        GPIO.setwarnings(False)

        self.__trigger_pin = trigger_pin
        self.__echo_pin = echo_pin

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.__trigger_pin, GPIO.OUT)
        GPIO.setup(self.__echo_pin, GPIO.IN)

    def send_trigger_pulse(self) -> None:
        GPIO.output(self.__trigger_pin, True)
        sleep(0.005)
        GPIO.output(self.__trigger_pin, False)

    def wait_for_echo(self, value, timeout) -> None:
        count = timeout

        while GPIO.input(self.__echo_pin) != value and count > 0:
            count = count - 1
     
    @property
    def distance(self) -> float:
        distance_cm = [0., 0., 0., 0., 0.]

        for i in range(5):
            self.send_trigger_pulse()

            self.wait_for_echo(True, 10000)
            start = time()
            self.wait_for_echo(False, 10000)

            finish = time()

            pulse_len = finish - start

            distance_cm[i] = pulse_len / 0.000058

        distance_cm = sorted(distance_cm)

        return distance_cm[2]

    @property
    def fast_distance(self) -> float:
        self.send_trigger_pulse()

        self.wait_for_echo(True, 10000)
        start = time()
        self.wait_for_echo(False, 10000)

        finish = time()

        pulse_len = finish - start

        return pulse_len / 0.000058
                
    