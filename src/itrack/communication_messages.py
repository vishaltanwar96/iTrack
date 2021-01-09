from . import constants

EMAIL_SUBJECT = {
    constants.NEW_TASK: "%s New Task Alert!" % constants.ITRACK_LABEL,
    constants.NEW_PROJECT_ASSOCIATION: "%s Welcome to the project!"
    % constants.ITRACK_LABEL,
    constants.USER_ACCOUNT_CREATED: "%s Welcome to iTrack!" % constants.ITRACK_LABEL,
    constants.RESEND_ACTIVATION_CODE: "%s Account Activation Code"
    % constants.ITRACK_LABEL,
    constants.ACCOUNT_CONFIRMATION: "%s Account Confirmed!" % constants.ITRACK_LABEL,
    constants.RESET_PASSWORD: "%s Password Assistance" % constants.ITRACK_LABEL,
    constants.TASK_HANDOVER: "%s Task Handover" % constants.ITRACK_LABEL,
}

EMAIL_BODY = {
    constants.NEW_TASK: (
        "Dear {assignee_first_name} {assignee_last_name},\n\n"
        "A new task has been assigned to you "
        "by {assignor_first_name} {assignor_last_name}\n\nDetails:\n"
        "Task ID: #{task_id}\nTask: {task_name}\n\n"
        "Please head to the portal for more details.\n\n"
        "%s" % constants.ITRACK_SIGNATURE
    ),
    constants.NEW_PROJECT_ASSOCIATION: (
        "Dear {user_first_name} {user_last_name},\n\n"
        "Welcome to the Project-{project_name}, We look forward for your contribution\n\n"
        "%s" % constants.ITRACK_SIGNATURE
    ),
    constants.USER_ACCOUNT_CREATED: (
        "Dear {user_first_name} {user_last_name},\n\n"
        "Your iTrack user account has been created, Please use the following code to activate your account.\n\n"
        "Code: {secret_key_signed_code}\n\n"
        "Note: The code expires in 2 days from the time received.\n\n%s"
        % constants.ITRACK_SIGNATURE
    ),
    constants.RESEND_ACTIVATION_CODE: (
        "Dear {user_first_name} {user_last_name},\n\n"
        "Please use the following code to activate your account.\n\n"
        "Code: {secret_key_signed_code}\n\n%s" % constants.ITRACK_SIGNATURE
    ),
    constants.ACCOUNT_CONFIRMATION: (
        "Dear {user_first_name} {user_last_name},\n\n"
        "Your iTrack account has been successfully confirmed\n\n%s"
        % constants.ITRACK_SIGNATURE
    ),
    constants.RESET_PASSWORD: (
        "Dear {user_first_name} {user_last_name},\n\n"
        "Please enter the code below to reset your password\n\n"
        "Code: {secret_key_signed_code}\n\n"
        "Note: The code expires in 2 days from the time received.\n\n%s"
        % constants.ITRACK_SIGNATURE
    ),
    constants.TASK_HANDOVER: (
        "Dear {new_assignee_first_name} {new_assignee_last_name},\n\n"
        "Task has been handed over from {old_assignee_first_name} {old_assignee_last_name} to you "
        "by {assignor_first_name} {assignor_last_name}\n\n"
        "Details:\n"
        "Task ID: #{task_id}\nTask: {task_name}\n\n"
        "Please head to the portal for more details.\n\n"
        "%s" % constants.ITRACK_SIGNATURE
    ),
}
