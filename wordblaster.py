import time

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

if __name__ == "__main__":
    device = MonkeyRunner.waitForConnection()

    device.touch(0, 0, MonkeyDevice.DOWN)
    time.sleep(1)

    coord = 0;

    while coord < 1080:
        device.touch(coord, coord, MonkeyDevice.MOVE)
        time.sleep(.1)
		coord = coord + 10

    device.touch(coord, coord, MonkeyDevice.UP)
