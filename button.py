import time # debounce timer (time.monotonic()).

from kivy.config import Config
# Kivy's Config controls: Must be set before other Kivy imports: 
# treat the mouse as a plain mouse and not draw the red "multitouch dot" on long presses
Config.set("input", "mouse", "mouse,disable_multitouch")

import gpiod # library that controls the Pi's GPIO pins.
from gpiod.line import Direction, Value # Direction (input or output) and Value (on or off)

from kivy.app import App # base class for every Kivy program
from kivy.uix.button import Button # clickable widget

from kivy.uix.floatlayout import FloatLayout # freely position and size UI elements

LED_PIN = 26
DEBOUNCE_SECONDS = 0.3 # how long to ignore extra taps after one registers


class LedApp(App): # Defines your app by inheriting from Kivy's App
    def build(self): # returns display (called once)
        # claims pin 26 from the GPIO system
        self.request = gpiod.request_lines(
            "/dev/gpiochip0",
            consumer="led-button",
            config={LED_PIN: gpiod.LineSettings(direction=Direction.OUTPUT)},
        )
        self.request.set_value(LED_PIN, Value.INACTIVE) # Starts with LED off.

        # variables: 
        self.led_on = False # tracks whether the LED is currently on
        self.last_toggle = 0.0 # records the time of the last accepted tap

        # Creates the button:
        self.button = Button(
            text="LED OFF",
            font_size=30,
            size_hint=(None, None),         # stop it from filling the window
            size=(200, 100),                # width, height in pixels
            pos_hint={"center_x": 0.5, "center_y": 0.5},  # center it
        )
        # when the button is released, Kivy calls self.toggle_led
        self.button.bind(on_release=self.toggle_led)

        layout = FloatLayout()
        layout.add_widget(self.button)
        # Hands the button to Kivy as the whole window's content.
        return layout

    # Runs on every release
    def toggle_led(self, button):
        # Button press if less than 0.3 seconds have passed
        # ignores duplicate touch/mouse events
        now = time.monotonic()
        if now - self.last_toggle < DEBOUNCE_SECONDS:
            return  
        self.last_toggle = now

        # Flips the remembered state on/off
        self.led_on = not self.led_on
        # sets the pin and updates display
        if self.led_on:
            self.request.set_value(LED_PIN, Value.ACTIVE)
            button.text = "ON"
        else:
            self.request.set_value(LED_PIN, Value.INACTIVE)
            button.text = "OFF"

    # window closes
    def on_stop(self):
        self.request.set_value(LED_PIN, Value.INACTIVE)
        self.request.release()

# Creates an instance of your app and starts it.
LedApp().run()
