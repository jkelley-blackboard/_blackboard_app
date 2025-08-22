import streamlit as st
import pandas as pd
import requests
from api_client import BlackboardAuth
from config import BLACKBOARD_KEY, BLACKBOARD_SECRET
from tasks import calendar, content, admins

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(page_title="Blackboard REST API Dashboard", layout="wide")

# Logo/Header
st.image(
    "https://www.anthology.com/imgs/logos/anthology-logo-black.svg",
    width=180  # smaller logo
)
st.title("📊 Blackboard REST API Dashboard")

# ----------------------------
# Sidebar Inputs (Left Column)
# ----------------------------
st.sidebar.header("Blackboard Configuration")

# Start with empty URL so user must enter it
bb_url = st.sidebar.text_input("Base URL", "")
test_mode = st.sidebar.checkbox("Run in Test Mode (no data committed to Blackboard)")
task = st.sidebar.selectbox(
    "Choose a task",
    ("Calendar Events", "Content Updates", "Assign Node Admins")
)

auth = None
system_version = None
url_valid = False  # Track if URL is validated

# ----------------------------
# URL Validation & Version Display
# ----------------------------
if bb_url:
    try:
        auth = BlackboardAuth(BLACKBOARD_KEY, BLACKBOARD_SECRET, bb_url)
        version_url = f"{bb_url}/learn/api/public/v1/system/version"
        resp = requests.get(version_url, headers=auth.headers(), timeout=10)
        if resp.status_code == 200:
            system_version = resp.json()
            learn = system_version.get("learn", {})
            major = learn.get("major", 0)
            minor = learn.get("minor", 0)
            patch = learn.get("patch", 0)
            build = learn.get("build", "N/A")

            st.sidebar.success("✅ URL validated")
            st.sidebar.info(f"Learn Version: {major}.{minor}.{patch} (build {build})")

            url_valid = True
        else:
            st.sidebar.error("❌ Unable to validate URL")
    except requests.exceptions.RequestException:
        st.sidebar.error("❌ Unable to connect to Blackboard. Check URL/network.")
    except Exception:
        st.sidebar.error("❌ Unable to connect to Blackboard.")

# ----------------------------
# Main Column: CSV Upload & Task Execution
# ----------------------------
if url_valid:
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("📂 Preview of Uploaded Data")
        st.dataframe(df.head())

        # Run Task button enabled only if CSV is uploaded
        run_task_button = st.button("Run Task")
        if run_task_button:
            if task == "Calendar Events":
                log = calendar.process(auth, df, test_mode)
            elif task == "Content Updates":
                log = content.process(auth, df, test_mode)
            elif task == "Assign Node Admins":
                log = admins.process(auth, df, test_mode)
            else:
                log = pd.DataFrame([{"status": "failed", "error": "Unknown task"}])

            st.subheader("📑 Processing Log")
            st.dataframe(log)

            # Save log file
            log_file = "processing_log.csv"
            log.to_csv(log_file, index=False)
            st.download_button(
                label="Download Log",
                data=log.to_csv(index=False),
                file_name="processing_log.csv",
                mime="text/csv",
            )
    else:
        st.info("⚠️ Upload a CSV file to enable task execution.")
else:
    st.info("⚠️ Please enter and validate a Blackboard URL to enable tasks.")
