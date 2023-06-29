import smbus
import time


class Adc:
    def __init__(self, addr: int = 0x48, pcf_addr: int = 0x40, ads_addr: int = 0x84):
        # Get I2C bus
        self.__bus = smbus.SMBus(1)

        # I2C address of the device
        self.__ADDRESS = addr

        # PCF8591 Command
        self.__PCF8591_CMD = pcf_addr  # Command

        # ADS7830 Command
        self.__ADS7830_CMD = ads_addr  # Single-Ended Inputs

        for i in range(3):
            aa = self.__bus.read_byte_data(self.__ADDRESS, 0xf4)
            if aa < 150:
                self.Index = "PCF8591"
            else:
                self.Index = "ADS7830"

    def analogReadPCF8591(self, chn) -> list:  # PCF8591 read ADC value,chn:0,1,2,3
        value = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(9):
            value[i] = self.__bus.read_byte_data(
                self.__ADDRESS, self.__PCF8591_CMD + chn)
        value = sorted(value)

        return value[4]

    def recvPCF8591(self, channel) -> float:  # PCF8591 write DAC value
        while True:
            # read the ADC value of channel 0,1,2,
            value1 = self.analogReadPCF8591(channel)
            value2 = self.analogReadPCF8591(channel)
            if value1 == value2:
                break
        voltage = value1 / 256.0 * 3.3  # calculate the voltage value
        voltage = round(voltage, 2)
        return voltage

    def recvADS7830(self, channel) -> float:
        """Select the Command data from the given provided value above"""
        COMMAND_SET = self.__ADS7830_CMD | (
            (((channel << 2) | (channel >> 1)) & 0x07) << 4)
        self.__bus.write_byte(self.__ADDRESS, COMMAND_SET)
        while True:
            value1 = self.__bus.read_byte(self.__ADDRESS)
            value2 = self.__bus.read_byte(self.__ADDRESS)
            if value1 == value2:
                break
        voltage = value1 / 255.0 * 3.3  # calculate the voltage value
        voltage = round(voltage, 2)

        return voltage

    def recvADC(self) -> dict:
        data: dict = {"LEFT": None, "RIGHT": None, "BATTERY": None}
        if self.Index == "PCF8591":
            data["LEFT"] = self.recvPCF8591(0)
            data["RIGHT"] = self.recvPCF8591(1)
            data["BATTERY"] = self.recvPCF8591(2)*3
        elif self.Index == "ADS7830":
            data["LEFT"] = self.recvADS7830(0)
            data["RIGHT"] = self.recvADS7830(1)
            data["BATTERY"] = self.recvADS7830(2)*3
        return data

    def i2cClose(self) -> None:
        self.__bus.close()
