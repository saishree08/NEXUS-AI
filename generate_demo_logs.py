import time
import random
from pathlib import Path
from datetime import datetime

# Location of the application log file
LOG_FILE = (
    Path(__file__).parent
    / "data"
    / "application.log"
)

# Create data folder if it does not exist
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# Sample application events
messages = [
    ("INFO", "Application service running successfully"),
    ("INFO", "Database connection established"),
    ("INFO", "User authentication successful"),

    ("WARNING", "CPU usage reached 82 percent"),
    ("WARNING", "Application response time is increasing"),
    ("WARNING", "Disk space is running low"),

    ("ERROR", "Database query execution failed"),
    ("ERROR", "Application request timeout"),

    ("CRITICAL", "Database connection lost"),
    ("CRITICAL", "Application service unavailable"),

    ("DEBUG", "Health check completed")
]

print("======================================")
print(" NEXUS AI - LIVE LOG GENERATOR")
print("======================================")

print("Log file:", LOG_FILE)
print("Generating new logs every 3 seconds...")
print("Press CTRL + C to stop.")
print("--------------------------------------")

try:

    while True:

        # Select a random log event
        severity, message = random.choice(messages)

        # Generate timestamp
        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Prepare log entry
        log_entry = (
            f"{timestamp} {severity} {message}"
        )

        # Append log to file
        with LOG_FILE.open(
            "a",
            encoding="utf-8"
        ) as file:

            file.write(log_entry + "\n")

        # Display generated event
        print(log_entry, flush=True)

        # Wait three seconds
        time.sleep(3)

except KeyboardInterrupt:

    print("\nNEXUS AI log generator stopped.")