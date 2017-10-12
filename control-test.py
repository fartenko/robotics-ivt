from pynput import keyboard
import threading

pin_16 = 0
pin_18 = 0

# pwm_16
# pwm_18 = GPIO.PWM ....

pwm_value = 0


def on_press(key):
    global pin_16, pin_18

    if key.char == 'w':
        pin_16 = 1
    if key.char == 's':
        pin_18 = 1

    print_states()
    # set_gpio()


def on_release(key):
    global pin_16, pin_18

    if key.char == 'w' or key.char == 's':
        pin_16 = 0
        pin_18 = 0

        print_states()
        set_gpio()


def print_states():
    print('pin16 => {0} ---- pin18 => {1}'.format(pin_16, pin_18))


def set_gpio():
    global pin_16, pin_18  # pwm_16, pwm_18
    # GPIO.output(16, pin_16)       # change frequency to 0
    # GPIO.output(18, pin_18)


# Collect events until released
def keyboard_controller():
    print('keyboard_controller started!')
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()


def pwm_controller():
    global pwm_value, pin_16, pin_18
    print('pwm_controller started!')
    while True:
        while pin_16 == 1:
            if pwm_value < 1024:
                pwm_value += 0.01
                print("pin16 __ PWM => {0}".format(round(pwm_value)))
        pwm_value = 0
        while pin_18 == 1:
            if pwm_value < 1024:
                pwm_value += 0.01
                print("pin18 __ PWM => {0}".format(round(pwm_value)))
        pwm_value = 0


def pwm_update():
    global pwm_value, pin_16, pin_18  # , pwm_16, pwm_18
    print('pwm_update started!')
    while True:
        # if pin_16 == 1: => freq on pwm_16 = pwm_value ... on 18 f = 0
        # if pin_18 == 1: => freq on pwm_18 = pwm_value ... on 16 f = 0
        pass


# def test_function():
#    print('test!')


try:
    threading.Thread(target=keyboard_controller).start()
    threading.Thread(target=pwm_controller).start()
    threading.Thread(target=pwm_update).start()
    # threading.Thread(target=test_function).start()
except EnvironmentError as e:
    print(e)
    print('Error: could not make threads')
