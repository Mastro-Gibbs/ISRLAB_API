import time
from rpi_ws281x import *
from enum import Enum


class Car_Arrow(Enum):
    LEFT = 0,
    RIGHT = 1,
    BACK = 2


class Led:
    __LED_COUNT = 8         # Number of LED pixels.
    __LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
    __LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    __LED_DMA = 10          # DMA channel to use for generating signal (try 10)
    __LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
    __LED_INVERT = False,   # True to invert the signal (when using NPN transistor level shift)
    __LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    __LED_ANIM_DELAY = 20
    __LED_ANIM_LOOPS = 5

    def __init__(self):
        # Control the sending order of color data
        self.ORDER = "RGB"
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(
            self.__LED_COUNT, self.__LED_PIN,
            self.__LED_FREQ_HZ, self.__LED_DMA,
            self.__LED_INVERT, self.__LED_BRIGHTNESS, self.__LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

    def LED_TYPR(self, order, R_G_B):
        B = R_G_B & 255
        G = R_G_B >> 8 & 255
        R = R_G_B >> 16 & 255
        Led_type = ["GRB", "GBR", "RGB", "RBG", "BRG", "BGR"]
        color = [Color(G, R, B), Color(G, B, R), Color(R, G, B),
                 Color(R, B, G), Color(B, R, G), Color(B, G, R)]
        if order in Led_type:
            return color[Led_type.index(order)]

    def colorWipe(self, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        color = self.LED_TYPR(self.ORDER, color)
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = pos * 3
            g = 255 - pos * 3
            b = 0
        elif pos < 170:
            pos -= 85
            r = 255 - pos * 3
            g = 0
            b = pos * 3
        else:
            pos -= 170
            r = 0
            g = pos * 3
            b = 255 - pos * 3
        return self.LED_TYPR(self.ORDER, Color(r, g, b))

    def rainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256*iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((i+j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def rainbowCycle(self, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256*iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel(
                    (int(i * 256 / self.strip.numPixels()) + j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)
        self.colorWipe(Color(0, 0, 0), 10)

    def car_arrow(self, ad: Car_Arrow):
        wait_s = 0.3

        if ad == Car_Arrow.LEFT:
            data = [3, 4, 5]
        elif ad == Car_Arrow.RIGHT:
            data = [0, 6, 7]
        else:
            data = [1, 2]

        off    = self.LED_TYPR(self.ORDER, Color(255, 100, 0))
        orange = self.LED_TYPR(self.ORDER, Color(0, 0, 0))

        while True:
            for index in data:
                self.strip.setPixelColor(index, orange)

            self.strip.show()
            time.sleep(wait_s)

            for index in data:
                self.strip.setPixelColor(index, off)

            self.strip.show()
            time.sleep(wait_s)

    def ledIndex(self, index, R, G, B):
        color = self.LED_TYPR(self.ORDER, Color(R, G, B))
        for i in range(8):
            if index & 0x01 == 1:
                self.strip.setPixelColor(i, color)
                self.strip.show()
            index = index >> 1
