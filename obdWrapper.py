import obd
import time


class ObdWrapper:
    def __init__(self):
        self.connection = obd.Async()
        self.connection.watch(obd.commands.FUEL_RATE)
        self.connection.watch(obd.commands.SPEED)
        self.connection.watch(obd.commands.CONTROL_MODULE_VOLTAGE)
        self.connection.watch(obd.commands.COOLANT_TEMP)
        self.connection.watch(obd.commands.ENGINE_LOAD)
        self.connection.watch(obd.commands.RPM)
        self.connection.start()
    
        self.distance_traveled = 0
        self.fuel_consumed = 0

        self.last_time = time.time()

    def get_instantaneous_mpg(self):
        speed = self.connection.query(obd.commands.SPEED).value
        fuel = self.connection.query(obd.commands.FUEL_RATE).value

        if speed is None or fuel is None:
            return 0

        speed = self.normalize(speed)
        fuel = self.normalize(fuel)

        time_stamp = time.time()
        dt = time_stamp - self.last_time
        self.distance_traveled += speed * dt
        self.fuel_consumed += fuel * dt
        self.last_time = time_stamp
        if fuel == 0:
            if speed == 0:
                return 0
            return 1000
        return speed/fuel
    
    def get_average_mpg(self):
        distance = self.distance_traveled
        fuel = self.fuel_consumed
        if fuel == 0:
            return 0
        return distance/fuel

    def get_speed(self):
        speed = self.connection.query(obd.commands.SPEED).value
        return self.normalize(speed)

    def get_voltage(self):
        voltage = self.connection.query(obd.commands.CONTROL_MODULE_VOLTAGE).value
        return self.normalize(voltage)
    
    def get_coolant_temp(self):
        temp = self.connection.query(obd.commands.COOLANT_TEMP).value
        return self.normalize(temp)

    def get_engine_load(self):
        load = self.connection.query(obd.commands.ENGINE_LOAD).value
        return self.normalize(load)
    
    def get_rpm(self):
        rpm = self.connection.query(obd.commands.RPM).value
        return self.normalize(rpm)
        
    def normalize(self, value):
        if value == None:
            return 0