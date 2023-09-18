# importing time and threading
import time
import threading
from pynput.mouse import Button, Controller

# pynput.keyboard is used to watch events of
# keyboard for start and stop of auto-clicker
from pynput.keyboard import Listener, KeyCode, Key

# four variables are created to
# control the auto-clicker
delay = 0.01
button = Button.left
start_stop_key = {Key.ctrl_l, Key.alt_l, KeyCode.from_char('j')}
stop_key = {Key.ctrl_l, Key.alt_l, KeyCode.from_char('m')}
current_keys_combination = set()

# threading.Thread is used
# to control clicks
class ClickMouse(threading.Thread):

    # delay and button are passed in the class
    # to check execution of auto-clicker
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True
        print("it runs")

    def stop_clicking(self):
        self.running = False
        print("it stopped")

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    # method to check and run loop until
    # it is true; another loop will check
    # if it is set to true or not,
    # for mouse click, it's set to button
    # and delay.
    def run(self):
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                time.sleep(self.delay)
            time.sleep(0.1)

# instance of mouse controller is created
mouse = Controller()
click_thread = ClickMouse(delay, button)
click_thread.start()

# on_press method takes
# key as an argument
def on_press(key):
    global listener  # Define listener as a global variable
    # start_stop_key will stop clicking
    # if the running flag is set to true
    if key in start_stop_key:
        current_keys_combination.add(key)
        if all(k in current_keys_combination for k in start_stop_key):
            if click_thread.running:
                click_thread.stop_clicking()
            else:
                click_thread.start_clicking()
    # here exit method is called and when
    # key is pressed, it terminates the auto clicker
    elif key in stop_key:
        current_keys_combination.add(key)
        if all(k in current_keys_combination for k in stop_key):
            click_thread.exit()
            listener.stop()


def on_release(key):
    try:
        current_keys_combination.remove(key)
    except KeyError:
        pass

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

