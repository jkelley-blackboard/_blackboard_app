import os
import pandas as pd
from datetime import datetime

def save_log(logs, task_name):
    """Save logs to a timestamped CSV file in logs/ directory."""
    if not os.path.exists("logs"):
        os.makedirs("logs")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"logs/{task_name}_{timestamp}.csv"

    log_df = pd.DataFrame(logs)
    log_df.to_csv(filename, index=False, encoding="utf-8")

    return filename
