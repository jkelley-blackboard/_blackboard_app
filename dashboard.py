import streamlit as st
import pandas as pd
import requests
from api_client import BlackboardAuth
from config import BLACKBOARD_KEY, BLACKBOARD_SECRET
from task_registry import TASK_REGISTRY

# ----------------------------
# Streamlit Page Setup
# ----------------------------
st.set_page_config(page_title="Blackboard REST API Dashboard", layout="wide")
st.image(
    "https://www.anthology.com/imgs/logos/anthology-logo-black.svg",
    width=180
)
st.title("📊 Blackboard REST API Dashboard")

# ----------------------------
# Sidebar Inputs
# ----------------------------
st.sidebar.header("Blackboard Configuration")

bb_url = st.sidebar.text_input("Base URL", "")
test_mode = st.sidebar.checkbox("Run in Test Mode (no data committed to Blackboard)")
task_name = st.sidebar.selectbox("Choose a task", list(TASK_REGISTRY.keys()))
task_obj = TASK_REGISTRY[task_name]

auth = None
url_valid = False

# ----------------------------
# URL Validation & Version Display
# ----------------------------
if bb_url:
    try:
        auth = BlackboardAuth(BLACKBOARD_KEY, BLACKBOARD_SECRET, bb_url)
        version_url = f"{bb_url}/learn/api/public/v1/system/version"
        resp = requests.get(version_url, headers=auth.headers(), timeout=10)
        if resp.status_code == 200:
            v = resp.json().get("learn", {})
            st.sidebar.success("✅ URL validated")
            st.sidebar.info(
                f"Learn Version: {v.get('major',0)}.{v.get('minor',0)}.{v.get('patch',0)} (build {v.get('build','N/A')})"
            )
            url_valid = True
        else:
            st.sidebar.error("❌ Unable to validate URL")
    except requests.exceptions.RequestException:
        st.sidebar.error("❌ Unable to connect to Blackboard. Check URL/network.")
    except Exception:
        st.sidebar.error("❌ Unable to connect to Blackboard.")

# ----------------------------
# Main Column: Data Input
# ----------------------------
if url_valid:
    st.subheader(f"{task_obj.name} Data Input")
    st.write(task_obj.description)

    input_method = st.radio("Input Method", ["Upload CSV", "Enter Data Manually"])
    df = None

    # ----------------------------
    # CSV Upload
    # ----------------------------
    if input_method == "Upload CSV":
        uploaded_file = st.file_uploader("Upload CSV", type="csv")
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.write("📂 Preview of Uploaded Data")
            st.dataframe(df.head())

    # ----------------------------
    # Manual Data Entry
    # ----------------------------
    elif input_method == "Enter Data Manually":
        df = st.data_editor(pd.DataFrame(columns=task_obj.columns), num_rows="dynamic")
        st.write("📂 Preview of Entered Data")
        st.dataframe(df)

    # ----------------------------
    # Run Task Button
    # ----------------------------
    if df is not None and not df.empty:
        if st.button("Run Task"):
            log = task_obj.process(auth, df, test_mode)
            st.subheader("📑 Processing Log")
            st.dataframe(log)

            # Download log
            st.download_button(
                label="Download Log",
                data=log.to_csv(index=False),
                file_name="processing_log.csv",
                mime="text/csv",
            )
    else:
        st.info("⚠️ Upload or enter data to enable task execution.")

else:
    st.info("⚠️ Please enter and validate a Blackboard URL to enable tasks.")
