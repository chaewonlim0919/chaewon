import serial

class MotorController:
    def __init__(self, port="/dev/ttyUSB0", baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
    
    def send_command(self, speed, steering_angle):
        command = f"{speed},{steering_angle}\n"
        self.ser.write(command.encode())

    def close(self):
        self.ser.close()
