import streamlit as st
import psutil
import os
from datetime import datetime

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

    uploaded_file = st.file_uploader(
        "Upload your infrastructure log file",
        type=["txt", "log", "csv"]
    )

    if uploaded_file is not None:

        st.success("File uploaded successfully!")

        st.write("File name:", uploaded_file.name)

        if uploaded_file.name.lower().endswith(".csv"):

            import pandas as pd

            df = pd.read_csv(uploaded_file)

            st.dataframe(df, use_container_width=True)

        else:

            content = uploaded_file.getvalue().decode(
                "utf-8",
                errors="replace"
            )

            st.text_area(
                "Log File Content",
                content,
                height=300
            )


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