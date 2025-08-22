import pandas as pd
import requests

def process(auth, df: pd.DataFrame, test_mode: bool = True) -> pd.DataFrame:
    """
    Assign observers using simple usernames in the table/file.
    The endpoint requires 'userName:' prefix, which is added automatically.
    
    Expected columns in df:
        - userName : e.g., "jkelley"
        - observerUserName : e.g., "jsmith"
    """
    log_records = []

    for _, row in df.iterrows():
        try:
            user = row.get("userName")
            observer = row.get("observerUserName")

            if not user or not observer:
                raise ValueError("Missing userName or observerUserName")

            # Add the required prefix for the API call
            user_prefixed = f"userName:{user}"
            observer_prefixed = f"userName:{observer}"

            url = f"{auth.base_url}/learn/api/public/v1/users/{user_prefixed}/observers/{observer_prefixed}"

            if test_mode:
                log_records.append({
                    "status": "test",
                    "userName": user,
                    "observerUserName": observer,
                    "url": url
                })
                continue

            resp = requests.put(url, headers=auth.headers())
            if resp.status_code in (200, 201):
                log_records.append({
                    "status": "success",
                    "userName": user,
                    "observerUserName": observer,
                    "response": resp.json()
                })
            else:
                log_records.append({
                    "status": "failed",
                    "userName": user,
                    "observerUserName": observer,
                    "response": resp.text
                })

        except Exception as e:
            log_records.append({
                "status": "failed",
                "userName": row.get("userName", ""),
                "observerUserName": row.get("observerUserName", ""),
                "error": str(e)
            })

    return pd.DataFrame(log_records)
