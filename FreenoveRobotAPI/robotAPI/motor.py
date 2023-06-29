from PCA9685 import PCA9685


class Motor:
    def __init__(self, PCA9685_i2c_addr: int = 0x40):
        """
        respect 12-bit rule, means duty must be -4096 < duty < 4096
        """
        self.__pca9685 = PCA9685(PCA9685_i2c_addr)
        self.__pca9685.setPWMFreq(50)
        
    def left_upper_wheel(self, duty) -> None:
        """
        -4096 < duty < 4096
        """
        if duty > 0:
            self.__pca9685.setMotorPwm(0, 0)
            self.__pca9685.setMotorPwm(1, duty)
        elif duty < 0:
            self.__pca9685.setMotorPwm(1, 0)
            self.__pca9685.setMotorPwm(0, abs(duty))
        else:
            self.__pca9685.setMotorPwm(0, 4095)
            self.__pca9685.setMotorPwm(1, 4095)

    def left_lower_wheel(self, duty) -> None:
        """
        -4096 < duty < 4095
        """
        if duty > 0:
            self.__pca9685.setMotorPwm(3, 0)
            self.__pca9685.setMotorPwm(2, duty)
        elif duty < 0:
            self.__pca9685.setMotorPwm(2, 0)
            self.__pca9685.setMotorPwm(3, abs(duty))
        else:
            self.__pca9685.setMotorPwm(2, 4095)
            self.__pca9685.setMotorPwm(3, 4095)

    def right_upper_wheel(self, duty) -> None:
        """
        -4096 < duty < 4096
        """
        if duty > 0:
            self.__pca9685.setMotorPwm(6, 0)
            self.__pca9685.setMotorPwm(7, duty)
        elif duty < 0:
            self.__pca9685.setMotorPwm(7, 0)
            self.__pca9685.setMotorPwm(6, abs(duty))
        else:
            self.__pca9685.setMotorPwm(6, 4095)
            self.__pca9685.setMotorPwm(7, 4095)

    def right_lower_wheel(self, duty) -> None:
        """
        -4096 < duty < 4096
        """
        if duty > 0:
            self.__pca9685.setMotorPwm(4, 0)
            self.__pca9685.setMotorPwm(5, duty)
        elif duty < 0:
            self.__pca9685.setMotorPwm(5, 0)
            self.__pca9685.setMotorPwm(4, abs(duty))
        else:
            self.__pca9685.setMotorPwm(4, 4095)
            self.__pca9685.setMotorPwm(5, 4095)


        
            

