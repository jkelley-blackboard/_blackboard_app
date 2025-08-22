# task_registry.py
from tasks import calendar, content, admins, observers

# ----------------------------
# Base Task class
# ----------------------------
class Task:
    name: str
    columns: list[str]
    description: str

    def process(self, auth, df, test_mode):
        raise NotImplementedError


# ----------------------------
# Calendar Task
# ----------------------------
class CalendarTask(Task):
    name = "Calendar Events"
    columns = ["external_course_key", "title", "description", "start", "end", "location"]
    description = "Create or update course calendar events."

    def process(self, auth, df, test_mode):
        return calendar.process(auth, df, test_mode)


# ----------------------------
# Content Task
# ----------------------------
class ContentTask(Task):
    name = "Content Updates"
    columns = ["course_id", "content_id", "description"]
    description = "Update course content descriptions."

    def process(self, auth, df, test_mode):
        return content.process(auth, df, test_mode)


# ----------------------------
# Admin Task
# ----------------------------
class AdminTask(Task):
    name = "Assign Node Admins"
    columns = ["external_course_key", "external_user_key", "system_role"]
    description = "Assign node administrators in Blackboard."

    def process(self, auth, df, test_mode):
        return admins.process(auth, df, test_mode)


# ----------------------------
# Observers Task
# ----------------------------
class ObserversTask(Task):
    name = "Assign Observers"
    columns = ["userName", "observerUserName"]
    description = (
        "Assign observers to users in Blackboard. "
        "Enter usernames only (e.g., jkelley, jsmith). The 'userName:' prefix is added automatically."
    )

    def process(self, auth, df, test_mode):
        return observers.process(auth, df, test_mode)


# ----------------------------
# Task Registry
# ----------------------------
TASK_REGISTRY = {
    t.name: t for t in [
        CalendarTask(),
        ContentTask(),
        AdminTask(),
        ObserversTask()
    ]
}
