MANAGER = "MANAGER"
CONTRIBUTOR = "CONTRIBUTOR"
LOW = "LOW"
MEDIUM = "MEDIUM"
HIGH = "HIGH"
SEVERE = "SEVERE"
ASSIGNED = "ASSIGNED"
WIP = "WIP"
ONHOLD = "ONHOLD"
INREVIEW = "IN-REVIEW"
# SCHEDULED = "SCHEDULED"
COMPLETED = "COMPLETED"
ABANDONED = "ABANDONED"
PLANNED = "PLANNED"
NEED_MORE_INFO = "NEED MORE INFO"

ITRACK_LABEL = "[iTrack]"
ITRACK_SIGNATURE = "Sincerely,\niTrack Notification Manager"

NEW_TASK = "NEW_TASK"
NEW_PROJECT_ASSOCIATION = "NEW_PROJECT_ASSOCIATION"
USER_ACCOUNT_CREATED = "USER_ACCOUNT_CREATED"
RESEND_ACTIVATION_CODE = "RESEND_ACTIVATION_CODE"
ACCOUNT_CONFIRMATION = "ACCOUNT_CONFIRMATION"
RESET_PASSWORD = "RESET_PASSWORD"
TASK_HANDOVER = "TASK_HANDOVER"

groups = (MANAGER, CONTRIBUTOR)
criticalities = (LOW, MEDIUM, HIGH, SEVERE)
statuses = (
    ASSIGNED,
    WIP,
    ONHOLD,
    INREVIEW,
    # SCHEDULED,
    COMPLETED,
    ABANDONED,
    PLANNED,
    NEED_MORE_INFO,
)

common_perms = [
    "view_user",
    "view_project",
    "add_projectremarkshistory",
    "view_projectremarkshistory",
    "add_task",
    "view_task",
    "add_taskremarkshistory",
    "view_taskremarkshistory",
    "add_todo",
    "change_todo",
    "delete_todo",
    "view_todo",
]
perms = {
    MANAGER: [
        "add_project",
        "change_project",
        "delete_project",
        "change_task",
        "delete_task",
    ]
    + common_perms,
    CONTRIBUTOR: common_perms,
}
