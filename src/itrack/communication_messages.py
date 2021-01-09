ITRACK_LABEL = "[iTrack]"
ITRACK_SIGNATURE = "Sincerely,\niTrack Notification Manager"

EMAIL_SUBJECT = {
    "NEW_TASK": "%s New Task Alert!" % ITRACK_LABEL,
    "NEW_PROJECT_ASSOCIATION": "%s Welcome to the project!" % ITRACK_LABEL,
    "USER_ACCOUNT_CREATED": "%s Welcome to iTrack!" % ITRACK_LABEL,
    "RESEND_ACTIVATION_CODE": "%s Account Activation Code" % ITRACK_LABEL,
    "ACCOUNT_CONFIRMATION": "%s Account Confirmed!" % ITRACK_LABEL,
    "RESET_PASSWORD": "%s Password Assistance" % ITRACK_LABEL,
}

EMAIL_BODY = {
    "NEW_TASK": (
        "Dear {assignee_first_name} {assignee_last_name},\n\n"
        "A new task has been assigned to you "
        "by {assignor_first_name} {assignor_last_name}\n\nDetails:\n"
        "Task ID: #{task_id}\nTask: {task_name}\n\n%s" % ITRACK_SIGNATURE
    ),
    "NEW_PROJECT_ASSOCIATION": (
        "Dear {user_first_name} {user_last_name},\n\n"
        "Welcome to the Project-{project_name}, We look forward for your contribution\n\n"
        "%s" % ITRACK_SIGNATURE
    ),
    "USER_ACCOUNT_CREATED": (
        "Dear {user_first_name} {user_last_name},\n\n"
        "Your iTrack user account has been created, Please use the following code to activate your account.\n\n"
        "Code: {secret_key_signed_code}\n\n"
        "Note: The code expires in 2 days from the time received.\n\n%s"
        % ITRACK_SIGNATURE
    ),
    "RESEND_ACTIVATION_CODE": (
        "Dear {user_first_name} {user_last_name},\n\n"
        "Please use the following code to activate your account.\n\n"
        "Code: {secret_key_signed_code}\n\n%s" % ITRACK_SIGNATURE
    ),
    "ACCOUNT_CONFIRMATION": (
        "Dear {user_first_name} {user_last_name},\n\n"
        "Your iTrack account has been successfully confirmed\n\n%s" % ITRACK_SIGNATURE
    ),
    "RESET_PASSWORD": (
        "Dear {user_first_name} {user_last_name},\n\n"
        "Please enter the code below to reset your password\n\n"
        "Code: {secret_key_signed_code}\n\n"
        "Note: The code expires in 2 days from the time received.\n\n%s"
        % ITRACK_SIGNATURE
    ),
}
