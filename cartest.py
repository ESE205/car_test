from picar import PiCar, test, configure
import time
import cv2
import argparse

parser = argparse.ArgumentParser(description="data for this program")
parser.add_argument('--mock_car',action='store_true',default=False,help='if not present, run on car, otherwise mock hardware')
args = parser.parse_args()

car = PiCar(mock_car=args.mock_car,threaded=True)

print(car)

print('Starting car forward')
car.set_motor(100)
time.sleep(3)
print('Starting car backwards')
car.set_motor(100, forward=False)
time.sleep(3)
print('Stopping car')
car.set_motor(0)
print('...')

print('Testing servos:')

car.set_swivel_servo(-5)
print(f'Swivel left: {car.swivel_servo_state}')
time.sleep(1)
car.set_swivel_servo(0)
print(f'Swivel center: {car.swivel_servo_state}')
time.sleep(1)
car.set_swivel_servo(5)
print(f'Swivel right: {car.swivel_servo_state}')
time.sleep(1)
car.set_swivel_servo(0)
time.sleep(1)

car.set_steer_servo(-5)
print(f'Steer left: {car.steer_servo_state}')
time.sleep(1)
car.set_steer_servo(0)
print(f'Steer center: {car.steer_servo_state}')
time.sleep(1)
car.set_steer_servo(5)
print(f'Steer right: {car.steer_servo_state}')
time.sleep(1)
car.set_steer_servo(0)
time.sleep(1)

car.set_nod_servo(-5)
print(f'Nod left: {car.nod_servo_state}')
time.sleep(1)
car.set_nod_servo(0)
print(f'Nod center: {car.nod_servo_state}')
time.sleep(1)
car.set_nod_servo(5)
print(f'Nod right: {car.nod_servo_state}')
time.sleep(1)
car.set_nod_servo(0)
time.sleep(1)
print('...')

print('Testing distance')
distance = car.read_distance()
print(f'Distance: {distance:0.3f}')
time.sleep(1)
print('...')

print('Testing camera')
camera = Picamera2()
camera.start()
array = camera.capture_array("main")
img = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
cv2.imwrite('testing.png',img)
print('image taken!')
time.sleep(1)
print('...')

print('Reading photoresistor')
print(f'{car.adc.read_adc(0)}')

print('Reading switch state')
print(f'{car.adc.read_adc(7)}')

print('done!')


