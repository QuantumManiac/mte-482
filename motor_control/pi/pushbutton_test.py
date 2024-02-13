import gpiozero

# Create a pushbutton object
pin = gpiozero.InputDevice(17, pull_up=True)

while True:
    print(f'{pin.value}')