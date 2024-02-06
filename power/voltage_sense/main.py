from gpiozero import InputDevice

volt_pin_7 = InputDevice(26)
volt_pin_8 = InputDevice(19, pull_up=False)
volt_pin_9 = InputDevice(13, pull_up=False)
volt_pin_10 = InputDevice(6)
volt_pin_11 = InputDevice(5)
volt_pin_12 = InputDevice(11, pull_up=False)

while True:
    print(f"{volt_pin_7.value}{volt_pin_8.value}{volt_pin_9.value}{volt_pin_10.value}{volt_pin_11.value}{volt_pin_12.value}")