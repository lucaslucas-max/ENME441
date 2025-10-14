import RPi.GPIO as GPIO
import time
from bugclass import Bug  # assuming your Bug class is in bug_class.py

# --- GPIO Pin setup for switches ---
S1_PIN = 17  # ON/OFF
S2_PIN = 27  # Toggle wrap
S3_PIN = 22  # Speed boost

GPIO.setmode(GPIO.BCM)
GPIO.setup(S1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(S2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(S3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# --- Instantiate the Bug ---
bug = Bug()  # uses default timestep=0.1, x=3, isWrapOn=False

# --- Internal state trackers ---
prev_s1 = GPIO.input(S1_PIN)
prev_s2 = GPIO.input(S2_PIN)
prev_s3 = GPIO.input(S3_PIN)
bug_running = False
default_timestep = bug.timestep

try:
    print("System ready. Use switches s1, s2, s3 to control the Bug.")
    while True:
        s1 = GPIO.input(S1_PIN)
        s2 = GPIO.input(S2_PIN)
        s3 = GPIO.input(S3_PIN)

        # --- s1: ON/OFF control ---
        if s1 and not bug_running:
            bug_running = True
            print("🐞 Bug started")
            # Run in background — use non-blocking loop
            bug._running = True
            while bug._running and GPIO.input(S1_PIN):  # keep bug alive while s1 is ON
                bug._Bug__update_display()  # call the Bug’s internal update
                time.sleep(bug.timestep)
                bug.x += 1 if GPIO.input(S3_PIN) else -1  # small motion example
                if bug.isWrapOn:
                    bug.x %= 8
                else:
                    bug.x = max(0, min(7, bug.x))
        elif not s1 and bug_running:
            bug.stop()
            bug_running = False
            print("🐞 Bug stopped")

        # --- s2: toggle wrapping (on state change) ---
        if s2 != prev_s2 and s2 == 1:
            bug.isWrapOn = not bug.isWrapOn
            print(f"🔁 Wrap mode toggled: {bug.isWrapOn}")

        # --- s3: speed control ---
        if s3 and not prev_s3:
            bug.timestep = default_timestep / 3
            print("⚡ Speed boosted (3x)")
        elif not s3 and prev_s3:
            bug.timestep = default_timestep
            print("🐢 Speed reset")

        # Save previous states
        prev_s1, prev_s2, prev_s3 = s1, s2, s3
        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nExiting program.")
    bug.stop()
    GPIO.cleanup()
