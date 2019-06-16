import spidev


class Mcp3008:
    def read_channel(self,channel):
        spi = spidev.SpiDev()
        spi.open(0, 0)
        spi.max_speed_hz = 10 ** 5
        datalist = [1, (8 + channel) << 4,0]
        bytes_in = spi.xfer2(datalist)
        a = bytes_in[1]
        b = bytes_in[2]
        result = a << 8 | b
        spi.close()
        return result