# import frappe
# from frappe.utils import now_datetime, add_to_date
# from frappe.core.doctype.communication.email import make
# from frappe.utils.background_jobs import enqueue

# def send_event_reminders():
#     now = now_datetime()
    
#     # Time intervals for reminders
#     reminder_times = {
#         "1_hour": add_to_date(now, hours=1),
#         "1_day": add_to_date(now, days=1),
#         "1_week": add_to_date(now, weeks=1),
#     }

#     # Fetch events with reminders enabled
#     events = frappe.get_all("Event", filters={"enable_reminder": 1}, fields=["name", "owner", "starts_on", "subject"])

#     for event in events:
#         event_time = frappe.utils.get_datetime(event["starts_on"])

#         for interval, reminder_time in reminder_times.items():
#             if event_time == reminder_time:
#                 send_notification(event, interval)

# def send_notification(event, interval):
#     """Send email notification for an event"""
#     user_email = frappe.get_value("User", event["owner"], "email")

#     if user_email:
#         subject = f"Reminder: {event['subject']} - {interval.replace('_', ' ')} away!"
#         message = f"Your event '{event['subject']}' is scheduled for {event['starts_on']}. This is a {interval.replace('_', ' ')} reminder."

#         make(
#             recipients=user_email,
#             sender=frappe.session.user,
#             subject=subject,
#             content=message,
#             send_email=True
#         )

#     frappe.msgprint(f"Sent reminder for Event: {event['name']} ({interval.replace('_', ' ')})")

