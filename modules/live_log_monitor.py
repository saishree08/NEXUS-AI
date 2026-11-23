from pathlib import Path
from datetime import datetime


LOG_FILE = (
    Path(__file__).parent.parent
    / "data"
    / "application.log"
)


def detect_severity(message):

    text = message.upper()

    if "CRITICAL" in text or "FATAL" in text:
        return "CRITICAL"

    elif "ERROR" in text or "FAILED" in text:
        return "ERROR"

    elif "WARNING" in text or "WARN" in text:
        return "WARNING"

    elif "DEBUG" in text:
        return "DEBUG"

    else:
        return "INFO"


def read_new_logs(previous_position=0):

    events = []

    if not LOG_FILE.exists():
        return events, previous_position

    try:

        with open(
            LOG_FILE,
            "r",
            encoding="utf-8",
            errors="replace"
        ) as file:

            file.seek(0, 2)
            file_size = file.tell()

            if file_size < previous_position:
                previous_position = 0

            file.seek(previous_position)

            new_lines = file.readlines()

            new_position = file.tell()

        for line in new_lines:

            message = line.strip()

            if not message:
                continue

            severity = detect_severity(message)

            events.append({
                "timestamp": datetime.now().strftime(
                    "%H:%M:%S"
                ),
                "severity": severity,
                "message": message
            })

        return events, new_position

    except Exception as error:

        print("Log monitoring error:", error)

        return events, previous_position