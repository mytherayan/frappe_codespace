import frappe
from frappe.utils import now_datetime, add_to_date

def send_event_reminders():
    now = now_datetime()
    events = frappe.get_all("Event", filters={"enable_reminders": 1}, fields=["name", "starts_on", "reminder_time", "custom_reminder_time", "owner"])

    for event in events:
        event_time = event.starts_on
        reminder_time = None

        if event.reminder_time == "1 Minute Before":
            reminder_time = add_to_date(event_time, minutes=-1)
        elif event.reminder_time == "1 Hour Before":
            reminder_time = add_to_date(event_time, hours=-1)
        elif event.reminder_time == "1 Day Before":
            reminder_time = add_to_date(event_time, days=-1)
        elif event.reminder_time == "1 Week Before":
            reminder_time = add_to_date(event_time, weeks=-1)
        elif event.reminder_time == "Custom" and event.custom_reminder_time:
            reminder_time = event.custom_reminder_time

        # Send reminder if the time matches
        if reminder_time and reminder_time <= now:
            send_notification(event.name, event.owner)

# def send_notification(event_name, recipient):
#     subject = f"Reminder: Upcoming Event {event_name}"
#     message = f"Your event '{event_name}' is scheduled soon. Don't forget to attend!"

#     # Send Frappe Notification
#     frappe.sendmail(recipients=recipient, subject=subject, message=message)

def send_notification(event_name, recipient):
    if not recipient:
        return "No recipient found"

    notification_doc = frappe.get_doc({
        "doctype": "Notification Log",
        "subject": f"Reminder: Upcoming Event - {event_name}",
        "email_content": f"Your event '{event_name}' is scheduled soon. Don't forget to attend!",
        "for_user": recipient,
        "type": "Alert",
        "document_type": "Event",
        "document_name": event_name,
    })

    notification_doc.insert(ignore_permissions=True)
    return "Notification Sent"
