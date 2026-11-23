import pandas as pd
import re
from io import StringIO


def process_uploaded_log(uploaded_file):

    filename = uploaded_file.name.lower()

    # Read CSV files
    if filename.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

        # Convert CSV rows into log messages
        if "message" in df.columns:
            messages = df["message"].fillna("").astype(str)
        elif "event" in df.columns:
            messages = df["event"].fillna("").astype(str)
        else:
            messages = df.fillna("").astype(str).agg(
                " | ".join, axis=1
            )

    # Read TXT and LOG files
    else:
        content = uploaded_file.getvalue().decode(
            "utf-8", errors="replace"
        )
        messages = pd.Series(content.splitlines())

    # Remove empty messages
    messages = messages.str.strip()
    messages = messages[messages != ""]

    # Remove duplicate messages
    messages = messages.drop_duplicates()

    records = []

    for message in messages:

        # Extract timestamp
        timestamp_match = re.search(
            r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}",
            message
        )

        timestamp = (
            timestamp_match.group(0)
            if timestamp_match
            else "Unknown"
        )

        # Identify severity
        severity_match = re.search(
            r"\b(CRITICAL|FATAL|ERROR|WARNING|WARN|INFO|DEBUG)\b",
            message,
            re.IGNORECASE
        )

        severity = (
            severity_match.group(0).upper()
            if severity_match
            else "UNKNOWN"
        )

        if severity == "WARN":
            severity = "WARNING"

        records.append({
            "Timestamp": timestamp,
            "Severity": severity,
            "Event": message
        })

    return pd.DataFrame(records)