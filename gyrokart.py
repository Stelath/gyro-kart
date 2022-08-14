import time
import board
import adafruit_mpu6050

import nxbt

i2c = board.I2C()  # uses board.SCL and board.SDA
mpu = adafruit_mpu6050.MPU6050(i2c)

# Start the NXBT service
print("Starting...")
nx = nxbt.Nxbt()

# Create a Pro Controller and wait for it to connect
# controller_index = nx.create_controller(nxbt.PRO_CONTROLLER)
print(nx.get_switch_addresses())
controller_index = nx.create_controller(
    nxbt.PRO_CONTROLLER,
    reconnect_address=nx.get_switch_addresses())
nx.wait_for_connection(controller_index)

print("Connected!")

while True:
    accel_x = mpu.acceleration[0]
    
    tilt = 0
    if accel_x > 0:
        if accel_x < 5:
            tilt = accel_x / 5 * 100
        else:
            tilt = 100
    else:
        if accel_x > -7:
            tilt = accel_x / 7 * 100
        else:
            tilt = -100
    
    print(f"Tilt: {tilt}")

    tilt = round(tilt)
    
    nx.tilt_stick(controller_index, nxbt.Sticks.LEFT_STICK, tilt, 0, tilted=abs(tilt / 200))
    
    accel_y = mpu.acceleration[1]
    if -(accel_y) > 15:
        print("jumped!")
        nx.press_buttons(controller_index, [nxbt.Buttons.Y], down=1.0)

# nx.remove_controller(controller_index)
