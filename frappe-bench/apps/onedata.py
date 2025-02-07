import frappe
from erpnext.crm.doctype.lead.lead import make_customer

@frappe.whitelist()
def bulk_convert_leads_to_customers(leads):
    leads = frappe.parse_json(leads)  # Convert JSON string to Python list
    success = []
    errors = []

    for lead_name in leads:
        try:
            customer_doc = make_customer(lead_name)  # Convert single lead
            customer_doc.insert(ignore_permissions=True)  # Save the new Customer
            frappe.db.set_value("Lead", lead_name, "status", "Converted")  # Update Lead Status
            success.append(lead_name)
        except Exception as e:
            errors.append(f"{lead_name}: {str(e)}")

    return {"success": success, "errors": errors}


