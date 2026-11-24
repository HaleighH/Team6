import time

from kivy.config import Config
# Must be set before other Kivy imports: stops mouse-emulated multitouch dots
Config.set("input", "mouse", "mouse,disable_multitouch")

import gpiod
from gpiod.line import Direction, Value

from kivy.app import App
from kivy.uix.button import Button

LED_PIN = 26
DEBOUNCE_SECONDS = 0.3


class LedApp(App):
    def build(self):
        self.request = gpiod.request_lines(
            "/dev/gpiochip0",
            consumer="led-button",
            config={LED_PIN: gpiod.LineSettings(direction=Direction.OUTPUT)},
        )
        self.request.set_value(LED_PIN, Value.INACTIVE)

        self.led_on = False
        self.last_toggle = 0.0

        self.button = Button(text="LED OFF", font_size=40)
        self.button.bind(on_release=self.toggle_led)
        return self.button

    def toggle_led(self, button):
        now = time.monotonic()
        if now - self.last_toggle < DEBOUNCE_SECONDS:
            return  # ignore duplicate touch/mouse events
        self.last_toggle = now

        self.led_on = not self.led_on
        if self.led_on:
            self.request.set_value(LED_PIN, Value.ACTIVE)
            button.text = "LED ON"
        else:
            self.request.set_value(LED_PIN, Value.INACTIVE)
            button.text = "LED OFF"

    def on_stop(self):
        self.request.set_value(LED_PIN, Value.INACTIVE)
        self.request.release()


LedApp().run()
