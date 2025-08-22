@echo off
REM ======================================================
REM Launch Blackboard Tools Dashboard
REM ======================================================

REM Change to project directory
cd /d "C:\Users\JeffKelley\OneDrive - Anthology Inc\a_Special_Projects\REST_API\_blackboard_app"

REM (Optional) Activate virtual environment if you use one
REM call venv\Scripts\activate

REM Start Streamlit dashboard
streamlit run dashboard.py --server.port=8501

pause