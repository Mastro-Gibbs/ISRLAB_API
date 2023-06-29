import time
import math
import smbus


# ============================================================================
# PCA9685 16-Channel PWM Servo Driver
# ============================================================================

class PCA9685:
    # Registers/etc.
    __SUBADR1 = 0x02
    __SUBADR2 = 0x03
    __SUBADR3 = 0x04
    __MODE1 = 0x00
    __PRESCALE = 0xFE
    __LED0_ON_L = 0x06
    __LED0_ON_H = 0x07
    __LED0_OFF_L = 0x08
    __LED0_OFF_H = 0x09
    __ALLLED_ON_L = 0xFA
    __ALLLED_ON_H = 0xFB
    __ALLLED_OFF_L = 0xFC
    __ALLLED_OFF_H = 0xFD

    def __init__(self, address=0x40):
        self.__bus = smbus.SMBus(1)
        self.__address = address
        self.__write(self.__MODE1, 0x00)

    def __write(self, reg, value):
        """Writes an 8-bit value to the specified register/address"""
        self.__bus.write_byte_data(self.__address, reg, value)

    def __read(self, reg):
        """Read an unsigned byte from the I2C device"""
        return self.__bus.read_byte_data(self.__address, reg)

    def setPWMFreq(self, freq):
        """Sets the PWM frequency"""
        prescaleval = 25000000.0  # 25MHz
        prescaleval /= 4096.0     # 12-bit
        prescaleval /= float(freq)
        prescaleval -= 1.0
        prescale = math.floor(prescaleval + 0.5)

        oldmode = self.__read(self.__MODE1)
        newmode = (oldmode & 0x7F) | 0x10    # sleep
        self.__write(self.__MODE1, newmode)  # go to zzz
        self.__write(self.__PRESCALE, int(math.floor(prescale)))
        self.__write(self.__MODE1, oldmode)
        time.sleep(0.005)
        self.__write(self.__MODE1, oldmode | 0x80)

    def __setPWM(self, channel, on, off):
        """Sets a single PWM channel"""
        self.__write(self.__LED0_ON_L + 4 * channel, on & 0xFF)
        self.__write(self.__LED0_ON_H + 4 * channel, on >> 8)
        self.__write(self.__LED0_OFF_L + 4 * channel, off & 0xFF)
        self.__write(self.__LED0_OFF_H + 4 * channel, off >> 8)

    def setMotorPwm(self, channel, duty):
        self.__setPWM(channel, 0, int(duty))

    def setServoPulse(self, channel, pulse):
        """Sets the Servo Pulse,The PWM frequency must be 50HZ"""
        pulse = pulse * 4096 / 20000  # PWM frequency is 50HZ,the period is 20000us
        self.__setPWM(channel, 0, int(pulse))
