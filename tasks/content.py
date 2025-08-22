def update_content(api, df, test_mode=False):
    logs = []
    for _, row in df.iterrows():
        external_id = row["course_external_id"]
        content_id = row["content_id"]

        try:
            resp = api.get(f"/learn/api/public/v1/courses?externalId={external_id}")
            results = resp.get("results", [])
            if not results:
                raise ValueError(f"No course found for externalId '{external_id}'")
            course_id = results[0]["id"]

            payload = {"description": row["description"]}

            if not test_mode:
                response = api.put(f"/learn/api/public/v1/courses/{course_id}/contents/{content_id}", payload)
                if response.get("status") not in [200, 201]:
                    logs.append({**row.to_dict(), "status": "failed", "error": str(response)})
                else:
                    logs.append({**row.to_dict(), "status": "success", "error": ""})
            else:
                logs.append({**row.to_dict(), "status": "success (test)", "error": ""})

        except Exception as e:
            logs.append({
                **row.to_dict(),
                "status": "failed",
                "error": f"{str(e)} | payload: {payload}"
            })

    return logs
