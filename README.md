# LMSK Scraper

A modular Python-based scraper for Moodle LMS, designed to extract courses, events, notifications, and calendar data, and sync them with the LMSK API.

## Project Structure

- **`main.py`**: The main entry point that runs the scraping loop.
- **`config.py`**: Contains configuration settings, including LMS credentials and API endpoints.
- **`api_client.py`**: A client for interacting with the LMSK API.
- **`scrapers/`**: Specialized scraper modules for different parts of Moodle.
  - `auth.py`: Handles authentication and session management.
  - `courses.py`: Extracts course information.
  - `events.py`: Extracts timeline events.
  - `notifications.py`: Extracts user notifications.
  - `calendar.py`: Downloads and parses calendar ICS files.
- **`utils/`**: Utility functions, such as ICS to JSON conversion.

## API Integration

The scraper is designed to send extracted data to the **LMSK API** (default: `http://127.0.0.1:5000`).

### Synchronized Data Types

1. **Metadata**: Sent to `/lmsk/metadata` after every scrape.
2. **Calendar Events**: Sent to `/lmsk/calender`.
3. **Timeline Events**: Sent to `/lmsk/event`.
4. **Courses**: Sent to `/lmsk/course`.

## Configuration

Settings can be managed in `config.py` or via environment variables:

- `LMS_USERNAME`: Your Moodle username.
- `LMS_PASSWORD`: Your Moodle password.
- `API_URL`: The base URL of the LMSK API.
- `API_ENABLED`: Set to `true` to enable syncing with the API.

## Running the Scraper

```bash
uv run main.py
```
The scraper will run indefinitely, performing a scrape every 3 hours (configurable in `main.py`).
