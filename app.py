import streamlit as st
import psutil
import os
from datetime import datetime
from modules.log_processor import process_uploaded_log
from modules.live_log_monitor import read_new_logs


# Configure the dashboard
st.set_page_config(
    page_title="NEXUS AI",
    page_icon="🧠",
    layout="wide"
)

# Dashboard heading
st.title("🧠 NEXUS AI")
st.subheader("Enterprise Autonomous Infrastructure Intelligence")
st.caption("AI-powered infrastructure monitoring and analysis platform")

st.divider()

# Sidebar navigation
st.sidebar.title("NEXUS AI")
st.sidebar.success("System Online")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home Dashboard",
        "Live System Monitoring",
        "Upload Infrastructure Logs",
        "Real-Time Log Monitoring",
        "AI Anomaly Detection",
        "Root Cause Analysis",
        "Predictive Failure Detection",
        "Self-Healing Center",
        "AI Assistant",
        "Incident Reports"
    ]
)

# Read Windows system metrics
def get_system_metrics():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent

    disk_path = (
        os.environ.get("SystemDrive", "C:") + "\\"
        if os.name == "nt"
        else "/"
    )

    disk = psutil.disk_usage(disk_path).percent

    return cpu, memory, disk


# Home dashboard
if page == "Home Dashboard":

    st.header("Infrastructure Overview")

    cpu, memory, disk = get_system_metrics()

    col1, col2, col3 = st.columns(3)

    col1.metric("CPU Usage", f"{cpu}%")
    col2.metric("RAM Usage", f"{memory}%")
    col3.metric("Disk Usage", f"{disk}%")

    st.divider()

    st.subheader("System Health")

    if cpu > 90 or memory > 90 or disk > 95:
        st.error("Critical resource usage detected!")

    elif cpu > 75 or memory > 75 or disk > 85:
        st.warning("Infrastructure needs attention.")

    else:
        st.success("System resources are within normal limits.")

    st.caption(
        "Last checked: "
        + datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    )


# Live monitoring
elif page == "Live System Monitoring":

    st.header("Live System Monitoring")

    if st.button("Refresh System Metrics"):

        cpu, memory, disk = get_system_metrics()

        st.metric("CPU Usage", f"{cpu}%")
        st.metric("RAM Usage", f"{memory}%")
        st.metric("Disk Usage", f"{disk}%")

        st.success("Metrics updated successfully!")

    else:
        st.info("Click the button to collect system metrics.")


# Upload logs
elif page == "Upload Infrastructure Logs":

    st.header("Upload Infrastructure Logs")

    st.subheader("NEXUS AI - Intelligent Log Processing")

    uploaded_file = st.file_uploader(
        "Upload your infrastructure log file",
        type=["txt", "log", "csv"],
        key="day2_log_upload"
    )

    if uploaded_file is not None:

        try:
            st.success("File uploaded successfully!")

            st.write("File name:", uploaded_file.name)

            # Process uploaded logs
            processed_logs = process_uploaded_log(uploaded_file)

            # Display total logs
            st.metric(
                "Total Clean Logs",
                len(processed_logs)
            )

            # Display processed logs
            st.subheader("Processed Infrastructure Logs")

            st.dataframe(
                processed_logs,
                width="stretch"
            )

            # Severity filter
            st.subheader("Filter Logs by Severity")

            selected_severity = st.selectbox(
                "Select Severity",
                [
                    "ALL",
                    "CRITICAL",
                    "ERROR",
                    "WARNING",
                    "INFO",
                    "DEBUG",
                    "UNKNOWN"
                ]
            )

            if selected_severity != "ALL":

                filtered_logs = processed_logs[
                    processed_logs["Severity"] == selected_severity
                ]

            else:
                filtered_logs = processed_logs

            st.subheader("Filtered Logs")

            st.dataframe(
                filtered_logs,
                width="stretch"
            )

        except Exception as e:

            st.error(f"Log processing failed: {e}")

elif page == "Real-Time Log Monitoring":

    st.header("Real-Time Infrastructure Log Monitoring")

    st.caption(
        "NEXUS AI continuously monitors incoming application logs."
    )

    # Initialize monitoring state
    if "log_position" not in st.session_state:
        st.session_state.log_position = 0

    if "live_events" not in st.session_state:
        st.session_state.live_events = []

    # Read new log entries
    new_events, new_position = read_new_logs(
        st.session_state.log_position
    )

    st.session_state.log_position = new_position

    # Store newly detected events
    if new_events:

        st.session_state.live_events.extend(new_events)

        # Keep only the latest 500 events
        st.session_state.live_events = (
            st.session_state.live_events[-500:]
        )

    events = st.session_state.live_events

    # Calculate statistics
    total_logs = len(events)

    error_count = sum(
        event["severity"] == "ERROR"
        for event in events
    )

    warning_count = sum(
        event["severity"] == "WARNING"
        for event in events
    )

    critical_count = sum(
        event["severity"] == "CRITICAL"
        for event in events
    )

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Events", total_logs)
    col2.metric("Errors", error_count)
    col3.metric("Warnings", warning_count)
    col4.metric("Critical", critical_count)

    st.divider()

    # Live event feed
    st.subheader("Incoming Log Events")

    if events:

        for event in reversed(events[-50:]):

            severity = event["severity"]

            if severity == "CRITICAL":
                st.error(
                    f'{event["timestamp"]} | '
                    f'{severity} | '
                    f'{event["message"]}'
                )

            elif severity == "ERROR":
                st.error(
                    f'{event["timestamp"]} | '
                    f'{severity} | '
                    f'{event["message"]}'
                )

            elif severity == "WARNING":
                st.warning(
                    f'{event["timestamp"]} | '
                    f'{severity} | '
                    f'{event["message"]}'
                )

            else:
                st.info(
                    f'{event["timestamp"]} | '
                    f'{severity} | '
                    f'{event["message"]}'
                )

    else:

        st.info(
            "Waiting for incoming logs... "
            "Start the demo log generator."
        )

    st.divider()

    if st.button("Clear Monitoring History"):

        st.session_state.live_events = []
        st.session_state.log_position = 0

        st.rerun()

        
# Other modules - to be developed
elif page == "AI Anomaly Detection":
    st.header("AI Anomaly Detection")
    st.info("Anomaly detection module is under development.")

elif page == "Root Cause Analysis":
    st.header("AI Root Cause Analysis")
    st.info("Root cause analysis module is under development.")

elif page == "Predictive Failure Detection":
    st.header("Predictive Failure Detection")
    st.info("Failure prediction module is under development.")

elif page == "Self-Healing Center":
    st.header("Self-Healing Center")
    st.info("Human-approved recovery recommendations will be developed here.")

elif page == "AI Assistant":
    st.header("NEXUS AI Assistant")
    st.info("AI assistant is under development.")

elif page == "Incident Reports":
    st.header("Incident Reports")
    st.info("Incident reporting module is under development.")

st.divider()

st.caption(
    "NEXUS AI | Infrastructure Intelligence | Version 1.0"
)