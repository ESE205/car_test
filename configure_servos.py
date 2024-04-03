from picar import PiCar, configure
import time
import argparse

car = PiCar(mock_car=False)
configure.configure_car(car)
