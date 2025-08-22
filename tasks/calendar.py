import pandas as pd
import traceback

def process_calendar(api, df: pd.DataFrame, test_mode: bool = False) -> pd.DataFrame:
    """
    Process calendar items from a CSV and create them in Blackboard.

    Expected CSV columns:
    - external_course_key
    - title
    - description
    - location
    - start
    - end
    """
    log_entries = []

    # Normalize headers
    df.columns = [c.strip() for c in df.columns]

    for _, row in df.iterrows():
        try:
            # Read external course key
            course_external_id = str(row.get("external_course_key", "")).strip()
            if not course_external_id:
                log_entries.append({
                    "status": "failed",
                    "courseExternalId": "",
                    "error": "Missing external_course_key in CSV row"
                })
                continue

            # 1️⃣ Lookup course using V3 endpoint
            course_resp = api.get(f"/learn/api/public/v3/courses/externalId:{course_external_id}")

            if course_resp.status_code != 200:
                log_entries.append({
                    "status": "failed",
                    "courseExternalId": course_external_id,
                    "error": f"Failed to resolve course externalId ({course_resp.status_code}): {course_resp.text}"
                })
                continue

            course_id = course_resp.json().get("id")
            if not course_id:
                log_entries.append({
                    "status": "failed",
                    "courseExternalId": course_external_id,
                    "error": "Course ID not found in response"
                })
                continue

            # 2️⃣ Build calendar payload
            payload = {
                "type": "Course",
                "calendarId": course_id,
                "title": row.get("title", ""),
                "description": row.get("description", ""),
                "location": row.get("location", ""),
                "start": row.get("start", ""),
                "end": row.get("end", "")
            }

            # 3️⃣ Handle Test Mode
            if test_mode:
                log_entries.append({
                    "status": "simulated",
                    "courseExternalId": course_external_id,
                    "payload": payload
                })
                continue

            # 4️⃣ Create calendar item and log full request/response
            calendar_endpoint = "/learn/api/public/v1/calendars/items"
            resp = api.post(calendar_endpoint, json=payload)

            # Capture full info for debugging
            log_entry = {
                "courseExternalId": course_external_id,
                "endpoint": api.auth.base_url + calendar_endpoint,
                "payload": payload,
                "status_code": resp.status_code,
                "response_text": resp.text
            }

            if resp.status_code in (200, 201):
                log_entry["status"] = "success"
                log_entry["calendarItemId"] = resp.json().get("id")
            else:
                log_entry["status"] = "failed"
            
            log_entries.append(log_entry)

        except Exception as e:
            log_entries.append({
                "status": "failed",
                "courseExternalId": row.get("external_course_key", ""),
                "error": str(e),
                "traceback": traceback.format_exc()
            })

    return pd.DataFrame(log_entries)
