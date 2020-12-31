EMAIL_SUBJECT = {
    "NEW_TASK": "[iTrack] New Task Alert!",
    "NEW_PROJECT_ASSOCIATION": "[iTrack] Welcome to the project!",
    "USER_ACCOUNT_CREATED": "[iTrack] Welcome to iTrack!",
    "RESEND_ACTIVATION_CODE": "[iTrack] Account Activation Code",
    "ACCOUNT_CONFIRMATION": "[iTrack] Account Confirmed!",
    "RESET_PASSWORD": "[iTrack] Password Assistance",
}

EMAIL_BODY = {
    "NEW_TASK": (
        "Dear {assignee_first_name} {assignee_last_name},\n"
        "A new task has been assigned to you "
        "by {assignor_first_name} {assignor_last_name}\n\nDetails:\n"
        "Task ID: #{task_id}\nTask: {task_name}\n\nSincerely\niTrack"
    ),
    "NEW_PROJECT_ASSOCIATION": (
        "Dear {user_first_name} {user_last_name},\n"
        "Welcome to the Project-{project_name}, We look forward for your contribution\n\n"
        "Sincerely\niTrack"
    ),
    "USER_ACCOUNT_CREATED": (
        "Dear {user_first_name} {user_last_name},\n"
        "Your iTrack user account has been created, Please use the following code to activate your account.\n\n"
        "Code: {secret_key_signed_code}\n\n"
        "Note: The code expires in 2 days from the time received.\n\n"
        "Sincerely\niTrack"
    ),
    "RESEND_ACTIVATION_CODE": (
        "Dear {user_first_name} {user_last_name},\n"
        "Please use the following code to activate your account.\n\n"
        "Code: {secret_key_signed_code}\n\n"
        "Sincerely\niTrack"
    ),
    "ACCOUNT_CONFIRMATION": (
        "Dear {user_first_name} {user_last_name},\n"
        "Your iTrack account has been successfully confirmed\n\n"
        "Sincerely\niTrack"
    ),
    "RESET_PASSWORD": (
        "Dear {user_first_name} {user_last_name},\n"
        "Please enter the code below to reset your password\n\n"
        "Code: {signing.dumps(user.id)}\n\n"
        "Note: The code expires in 2 days from the time received.\n\n"
        "Sincerely\niTrack"
    ),
}
