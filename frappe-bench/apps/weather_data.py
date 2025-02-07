import frappe
import requests
from frappe.utils import now

API_KEY = "738c25c0c7891f2a902f1b589615ef04"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@frappe.whitelist()
def fetch_weather(city="tirupur"):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data.get("cod") != 200:
            frappe.throw(f"Error fetching weather: {data.get('message')}")

        weather_info = {
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather_description": data["weather"][0]["description"],
            "timestamp": now(),
        }

        weather_doc = frappe.get_doc({
            "doctype": "Weather Data",
            **weather_info
        })
        weather_doc.insert(ignore_permissions=True)
        frappe.db.commit()
        frappe.msgprint(f"Weather data for {city} saved successfully!")

    except Exception as e:
        frappe.log_error(f"Weather Fetch Error: {str(e)}", "Weather Integration")

