# URL Shortener Service

A simple REST API backend for shortening URLs, built with Python and Flask. Uses SQLite for storage and supports link expiry.

## Features

- Shorten any long URL to a 6-character code
- Redirect to original URL using the short code
- Links expire after 30 days by default (configurable)
- Returns HTTP 410 Gone for expired links
- View info about any shortened URL
- List all shortened URLs

## Tech Stack

- Python
- Flask
- SQLite
- REST APIs

## Project Structure

```
url_shortener/
│
├── app.py            # main application with all routes
├── urls.db           # SQLite database (auto-created on first run)
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repo
```bash
git clone https://github.com/your-username/url-shortener.git
cd url-shortener
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the app
```bash
python app.py
```

Server starts at `http://localhost:5000`

## API Endpoints

### POST /shorten
Shorten a URL.

**Request:**
```json
{
  "url": "https://www.example.com/some/very/long/url",
  "expires_in_days": 30
}
```

**Response:**
```json
{
  "short_code": "aB3xYz",
  "short_url": "http://localhost:5000/aB3xYz",
  "expires_at": "2026-06-06 14:30:00"
}
```

---

### GET /<short_code>
Redirects to the original URL.

- Returns `302 Redirect` if valid
- Returns `404` if code not found
- Returns `410 Gone` if link has expired

---

### GET /info/<short_code>
Get details about a shortened URL without redirecting.

**Response:**
```json
{
  "short_code": "aB3xYz",
  "original_url": "https://www.example.com/some/very/long/url",
  "created_at": "2026-05-07 14:30:00",
  "expires_at": "2026-06-06 14:30:00"
}
```

---

### GET /all
List all shortened URLs.

## How the Short Code Works

A 6-character code is randomly generated from 62 characters (a-z, A-Z, 0-9). This gives 62^6 = over 56 billion possible combinations, making collisions extremely unlikely. If a collision does occur, the app keeps generating until it finds a unique code.

## Design Decisions

- **SQLite** was chosen for simplicity and zero setup overhead
- **Base62 character set** keeps codes short, URL-safe, and readable
- **Expiry** is stored as a timestamp and checked on every redirect request
- **Modular route structure** keeps each endpoint single-responsibility
