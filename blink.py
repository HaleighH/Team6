import time
import gpiod
from gpiod.line import Direction, Value

LED_PIN = 26

with gpiod.request_lines(
    "/dev/gpiochip0",
    consumer="blink",
    config={LED_PIN: gpiod.LineSettings(direction=Direction.OUTPUT)},
) as request:
    print(f"Blinking LED connected to GPIO pin {LED_PIN}")
    try:
        while True:  # Ctrl+C to end
            request.set_value(LED_PIN, Value.ACTIVE)
            time.sleep(0.5)

            request.set_value(LED_PIN, Value.INACTIVE)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nStopped")
