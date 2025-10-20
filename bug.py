# bug.py
import time
import RPi.GPIO as GPIO
from bugclass import Bug

# GPIO pins for switches
S1_PIN = 17  # Start/Stop
S2_PIN = 27  # Toggle wrap mode
S3_PIN = 22  # Speed boost

GPIO.setmode(GPIO.BCM)
GPIO.setup(S1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(S2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(S3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

bug = Bug()
default_timestep = bug.timestep
boosted_timestep = default_timestep / 3
prev_s2 = GPIO.input(S2_PIN)

try:
    print("Bug control running. Press Ctrl+C to quit.")
    print("S1: on/off | S2: toggle wrap | S3: speed boost")

    while True:
        s1 = GPIO.input(S1_PIN)
        s2 = GPIO.input(S2_PIN)
        s3 = GPIO.input(S3_PIN)

        # --- S1: Start or stop bug ---
        if s1 and not bug._running:
            bug.start()
            print("Bug started.")
        elif not s1 and bug._running:
            bug.stop()
            print("Bug stopped.")

        # --- S2: Toggle wrap mode on rising edge ---
        if s2 != prev_s2 and s2 == 1:
            bug.isWrapOn = not bug.isWrapOn
            print(f"Wrap mode is now {'ON' if bug.isWrapOn else 'OFF'}")
        prev_s2 = s2

        # --- S3: Speed boost while held ---
        if s3:
            bug.timestep = boosted_timestep
        else:
            bug.timestep = default_timestep

        time.sleep(0.05)

except KeyboardInterrupt:
    print("Exiting program...")
finally:
    bug.stop()
    GPIO.cleanup()
