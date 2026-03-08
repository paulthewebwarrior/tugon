# Nagkakaisang Tugon Party Alliance Website

Modern Flask campaign website for the Engineering Student Council slate of the Nagkakaisang Tugon Party Alliance.

## Features

- Responsive Bootstrap 5 frontend with custom yellow-to-white campaign styling
- Candidate listing page with detailed Bootstrap profile modals
- Party platform, about, and contact pages
- Candidate data and contact submissions stored in JSON files
- Candidate photos served from `static/images`
- Optional home page background music from `static/audio/home-song.mp3`

## Project Structure

```text
tugon/
|-- app.py
|-- requirements.txt
|-- data/
|   |-- candidates.json
|   `-- messages.json
|-- static/
|   |-- css/styles.css
|   |-- js/main.js
|   |-- audio/
|   `-- images/
|-- templates/
|   |-- base.html
|   |-- index.html
|   |-- candidates.html
|   |-- platform.html
|   |-- about.html
|   `-- contact.html
`-- README.md
```

## Run Locally

1. Create and activate a virtual environment.
1. Install dependencies:

```bash
pip install -r requirements.txt
```

1. Start the development server:

```bash
python app.py
```

1. Open `http://127.0.0.1:5000`.

## Home Page Song Setup

1. Put your song file at `static/audio/home-song.mp3`.
1. Start the app and open the home page (`/`).

The song is only initialized on the home page. Depending on browser autoplay rules,
playback may begin immediately or after the first user interaction (click/key/touch).
