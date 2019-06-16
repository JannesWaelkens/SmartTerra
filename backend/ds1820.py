class Ds1820:

    def __init__(self,sensor_file_name='/sys/bus/w1/devices/28-011317695a93/w1_slave'):
        self.sensor_file_name = sensor_file_name
        self.__temperature = 0.0
        self.test = 'bla'

    def temperature(self):
        sensor_file = None
        try:
            sensor_file = open(self.sensor_file_name, 'r')
            for line in sensor_file:
                pos = line.find('t=')
                if pos != -1:
                    string_temperature = line[pos:]
                    self.__temperature = float(string_temperature[2:]) / 1000


        except Exception  as e:
            print(e)
        finally:
            if sensor_file != None:
                sensor_file.close()
            return  self.__temperature

    def __str__(self):
        return "De temperatuur is {} \N{DEGREE SIGN} Celsius".format(self.temperature)

if  __name__ == '__main__':
    sensor = Ds1820()
    print(sensor)
