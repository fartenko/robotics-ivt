from pynput import keyboard

pin_16 = 0
pin_18 = 0


def on_press(key):
    global pin_16, pin_18

    if key.char == 'w':
        pin_16 = 1
    if key.char == 's':
        pin_18 = 1

    print_states()
    set_gpio()


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
    global pin_16, pin_18
    # GPIO.output(16, pin_16)
    # GPIO.output(18, pin_18)


# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
