def assign_admins(api, df, test_mode=False):
    logs = []
    for _, row in df.iterrows():
        node_id = row["node_id"]
        user_id = row["user_id"]
        role = row["system_role"]

        payload = {"systemRole": role}

        try:
            if not test_mode:
                response = api.put(f"/learn/api/public/v1/institutionalHierarchy/nodes/{node_id}/admins/{user_id}", payload)
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
