import json
import html
from icalendar import Calendar
from datetime import datetime


def ics_to_json(ics_content):
    """
    Return all events from the iCalendar (.ics) content as a list of dictionaries.
    """
    events = []
    try:
        gcal = Calendar.from_ical(ics_content)
        for component in gcal.walk():
            if component.name == "VEVENT":
                # Extract and clean fields
                summary = str(component.get("summary", ""))
                description = str(component.get("description", ""))

                # Unescape HTML entities (e.g., &amp;)
                summary = html.unescape(summary)
                description = html.unescape(description)

                # Handle categories (convert to comma-separated string for DB)
                categories_data = component.get("categories", "")
                if categories_data:
                    if isinstance(categories_data, list):
                        categories = ", ".join([str(cat) for cat in categories_data])
                    else:
                        if hasattr(categories_data, "to_ical"):
                            categories = categories_data.to_ical().decode("utf-8")
                        else:
                            categories = str(categories_data)
                else:
                    categories = ""

                event = {
                    "uid": str(component.get("uid", "")),
                    "summary": summary,
                    "description": description,
                    "last_modified": format_date(component.get("last-modified").dt) if component.get("last-modified") else None,
                    "dt_stamp": format_date(component.get("dtstamp").dt) if component.get("dtstamp") else None,
                    "dt_start": (
                        format_date(component.get("dtstart").dt)
                        if component.get("dtstart")
                        else None
                    ),
                    "dt_end": (
                        format_date(component.get("dtend").dt)
                        if component.get("dtend")
                        else None
                    ),
                    "categories": categories,
                }
                events.append(event)
    except Exception as e:
        print(f"Error parsing ICS file: {e}")

    return events


def format_date(dt):
    """
    Formats a datetime object to an ISO 8601 string.
    """
    if isinstance(dt, datetime):
        return dt.isoformat()
    return str(dt)


if __name__ == "__main__":
    import sys
    import os

    # Default to Data/calendar.ics if it exists
    default_path = os.path.join("Data", "calendar.ics")
    path = sys.argv[1] if len(sys.argv) > 1 else default_path

    if os.path.exists(path):
        with open(path, "rb") as f:
            content = f.read()
        parsed_events = ics_to_json(content)
        print(json.dumps(parsed_events, indent=4))
    else:
        print(f"File not found: {path}")
