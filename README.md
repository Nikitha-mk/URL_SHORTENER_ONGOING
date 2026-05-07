# URL Shortener Service

A simple backend service that converts long URLs into short, shareable links. Built using Python, Flask, and SQLite.

## Features

* Generates 6-character short URLs
* Redirects to the original URL
* Links expire after 30 days
* Expired links return `410 Gone`
* View URL info without redirecting
* List all stored URLs

## Tech Stack

* Python
* Flask
* SQLite
* REST APIs

## Run Locally

```bash
pip install -r requirements.txt
python app.py
```

Runs on:

```bash
http://localhost:5000
```

## Endpoints

* `POST /shorten` → Create short URL
* `GET /<code>` → Redirect to original URL
* `GET /info/<code>` → Get URL details
* `GET /all` → List all URLs

## Short Code Logic

Short codes use random Base62 characters (`a-z`, `A-Z`, `0-9`).
With `62^6` combinations, collisions are very unlikely.

## Design Choices

* SQLite for simple zero-setup storage
* Base62 for short and URL-safe links
* Expiry checked during redirects
* Single-file structure for simplicity
