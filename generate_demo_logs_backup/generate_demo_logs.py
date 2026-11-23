import time
import random
from pathlib import Path
from datetime import datetime

LOG_FILE = Path(__file__).parent / "data" / "application.log"

LOG_FILE.parent.mkdir(exist_ok=True)

messages = [
    ("INFO", "Application service running successfully"),
    ("INFO", "Database connection established"),
    ("WARNING", "CPU usage reached 82 percent"),
    ("WARNING", "Application response time is increasing"),
    ("ERROR", "Database query execution failed"),
    ("ERROR", "Application request timeout"),
    ("CRITICAL", "Database connection lost"),
    ("CRITICAL", "Application service unavailable"),
    ("DEBUG", "Health check completed")
]

print("NEXUS AI Demo Log Generator Started")
print("Writing live events to:", LOG_FILE)
print("Press Ctrl+C to stop.")

try:
    while True:

        severity, message = random.choice(messages)

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        log_entry = (
            f"{timestamp} {severity} {message}\n"
        )

        with LOG_FILE.open("a", encoding="utf-8") as file:
            file.write(log_entry)

        print(log_entry.strip())

        time.sleep(3)

except KeyboardInterrupt:
    print("\nDemo log generator stopped.")