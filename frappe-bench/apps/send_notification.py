import frappe

@frappe.whitelist()
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
