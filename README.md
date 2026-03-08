# Nagkakaisang Tugon Party Alliance Website

Modern Flask campaign website for the Nagkakaisang Tugon Party Alliance, now built as a multi-council university political platform.

## Features

- Responsive Bootstrap 5 frontend with custom yellow-to-white campaign styling
- Multi-council candidate management (CSC, COESC, CASSC, CBASC, CFADSC)
- Council-specific pages with candidates and General Plan of Action (GPOA)
- Candidate profile pages with credentials and council-linked GPOA
- Candidate search by name/position and council filter
- Home page council selector, candidate spotlight, and election countdown
- Alliance platform, gallery, about, and contact pages
- Candidate data and contact submissions stored in JSON files
- Candidate photos served from `static/images`

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
|   `-- images/
|-- templates/
|   |-- base.html
|   |-- council.html
|   |-- candidate_profile.html
|   |-- index.html
|   |-- candidates.html
|   |-- platform.html
|   |-- gallery.html
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

## Core Routes

- `/` Home page with council selector, spotlight, countdown, and gallery preview
- `/candidates` Candidate directory with search and council filter
- `/candidate/<candidate_id>` Candidate profile page
- `/council/csc` Central Student Council page
- `/council/engineering` College of Engineering Student Council page
- `/council/arts_science` College of Arts and Science Student Council page
- `/council/business_admin` College of Business and Administration Student Council page
- `/council/fine_arts` College of Fine Arts, Architecture and Design Student Council page
- `/platform` Alliance platform page
- `/gallery` Campaign gallery