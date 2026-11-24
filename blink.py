import gpiod
from gpiod.line import Direction, Value

from kivy.app import App
from kivy.uix.togglebutton import ToggleButton

LED_PIN = 26


class LedApp(App):
    def build(self):
        self.request = gpiod.request_lines(
            "/dev/gpiochip0",
            consumer="led-button",
            config={LED_PIN: gpiod.LineSettings(direction=Direction.OUTPUT)},
        )
        self.request.set_value(LED_PIN, Value.INACTIVE)

        self.button = ToggleButton(text="LED OFF", font_size=40)
        self.button.bind(state=self.toggle_led)
        return self.button

    def toggle_led(self, button, state):
        if state == "down":
            self.request.set_value(LED_PIN, Value.ACTIVE)
            button.text = "LED ON"
        else:
            self.request.set_value(LED_PIN, Value.INACTIVE)
            button.text = "LED OFF"

    def on_stop(self):
        self.request.set_value(LED_PIN, Value.INACTIVE)
        self.request.release()


LedApp().run()
