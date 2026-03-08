from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path
from typing import Any

from flask import Flask, flash, redirect, render_template, request, url_for


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CANDIDATES_FILE = DATA_DIR / "candidates.json"
MESSAGES_FILE = DATA_DIR / "messages.json"


COUNCILS: list[dict[str, Any]] = [
    {
        "code": "CSC",
        "slug": "csc",
        "name": "Central Student Council",
        "short_name": "CSC",
        "description": "University-wide student leadership focused on institutional representation and student rights.",
        "positions": ["President", "Vice President", "Secretary", "Treasurer", "Auditor", "PRO"],
        "gpoa": [
            {"title": "Academic Programs", "icon": "bi-journal-check", "description": "Academic policy feedback loops and student consultation forums."},
            {"title": "Student Welfare", "icon": "bi-heart-pulse", "description": "Campus-wide welfare desks, referral systems, and emergency support channels."},
            {"title": "Facilities Improvement", "icon": "bi-building-check", "description": "Cross-college facility audits and student-priority improvement endorsements."},
            {"title": "Student Representation", "icon": "bi-people", "description": "Regular assemblies and transparent policy updates for all colleges."},
            {"title": "Innovation and Development", "icon": "bi-lightbulb", "description": "Digital student services and data-driven governance initiatives."},
        ],
    },
    {
        "code": "COESC",
        "slug": "engineering",
        "name": "College of Engineering Student Council",
        "short_name": "COESC",
        "description": "Engineering-focused council promoting technical growth, welfare, and transparent governance.",
        "positions": ["President", "Vice President", "Secretary", "Treasurer", "Auditor", "PRO"],
        "gpoa": [
            {"title": "Academic Programs", "icon": "bi-journal-check", "description": "Review sessions, peer mentoring, and skills-oriented learning support."},
            {"title": "Student Welfare", "icon": "bi-heart-pulse", "description": "Accessible welfare concerns channels and responsive support coordination."},
            {"title": "Facilities Improvement", "icon": "bi-building-check", "description": "Laboratory, classroom, and student-space enhancement initiatives."},
            {"title": "Student Representation", "icon": "bi-people", "description": "Year-level feedback integration for policy and project planning."},
            {"title": "Innovation and Development", "icon": "bi-cpu", "description": "Engineering innovation showcases and industry-aligned activities."},
        ],
    },
    {
        "code": "CASSC",
        "slug": "arts_science",
        "name": "College of Arts and Science Student Council",
        "short_name": "CASSC",
        "description": "Council for liberal arts and sciences centered on inclusive representation and interdisciplinary growth.",
        "positions": ["President", "Vice President", "Secretary", "Treasurer", "Auditor", "PRO"],
        "gpoa": [
            {"title": "Academic Programs", "icon": "bi-book", "description": "Research forums, writing clinics, and program-based enrichment tracks."},
            {"title": "Student Welfare", "icon": "bi-heart", "description": "Holistic support programs for student well-being and inclusion."},
            {"title": "Facilities Improvement", "icon": "bi-building", "description": "Learning-space optimization and equipment accessibility improvements."},
            {"title": "Student Representation", "icon": "bi-people", "description": "Cross-department consultations and participatory student governance."},
            {"title": "Innovation and Development", "icon": "bi-lightbulb", "description": "Creative and scientific collaboration platforms for student projects."},
        ],
    },
    {
        "code": "CBASC",
        "slug": "business_admin",
        "name": "College of Business and Administration Student Council",
        "short_name": "CBASC",
        "description": "Business council promoting leadership, entrepreneurship, and student-centered services.",
        "positions": ["President", "Vice President", "Secretary", "Treasurer", "Auditor", "PRO"],
        "gpoa": [
            {"title": "Academic Programs", "icon": "bi-briefcase", "description": "Certification support, case competitions, and internship readiness."},
            {"title": "Student Welfare", "icon": "bi-heart-pulse", "description": "Accessible welfare systems tailored to business student concerns."},
            {"title": "Facilities Improvement", "icon": "bi-building-check", "description": "Learning hub upgrades and resource center improvements."},
            {"title": "Student Representation", "icon": "bi-people", "description": "Open consultation mechanisms for policy and event planning."},
            {"title": "Innovation and Development", "icon": "bi-graph-up-arrow", "description": "Entrepreneurship labs and startup-oriented learning initiatives."},
        ],
    },
    {
        "code": "CFADSC",
        "slug": "fine_arts",
        "name": "College of Fine Arts, Architecture and Design Student Council",
        "short_name": "CFADSC",
        "description": "Creative council championing design excellence, student welfare, and collaborative culture.",
        "positions": ["President", "Vice President", "Secretary", "Treasurer", "Auditor", "PRO"],
        "gpoa": [
            {"title": "Academic Programs", "icon": "bi-pencil-square", "description": "Critique sessions, portfolio development, and professional design coaching."},
            {"title": "Student Welfare", "icon": "bi-heart", "description": "Student support systems balancing studio life and wellness."},
            {"title": "Facilities Improvement", "icon": "bi-house-gear", "description": "Studio upgrades and better access to design resources and spaces."},
            {"title": "Student Representation", "icon": "bi-people", "description": "Inclusive representation across art, architecture, and design programs."},
            {"title": "Innovation and Development", "icon": "bi-palette", "description": "Creative innovation programs and interdisciplinary project showcases."},
        ],
    },
]

COUNCIL_BY_CODE = {c["code"]: c for c in COUNCILS}
COUNCIL_BY_SLUG = {c["slug"]: c for c in COUNCILS}


SEED_MULTI_COUNCIL_CANDIDATES: list[dict[str, Any]] = [
    {
        "id": "csc-kate-de-villa",
        "name": "Kate De Villa",
        "position": "President",
        "photo": "images/default-candidate.svg",
        "credentials": "Student Leader Awardee\nFormer College Representative\nCampus Policy Forum Moderator",
        "plan_of_action": "Lead campus-wide policy consultations, strengthen welfare systems, and publish regular governance reports.",
        "council": "CSC",
        "created_at": "2026-03-08",
    },
    {
        "id": "csc-miguel-santos",
        "name": "Miguel Santos",
        "position": "Vice President",
        "photo": "images/default-candidate.svg",
        "credentials": "Leadership Congress Delegate\nUniversity Event Coordinator\nPeer Mentor",
        "plan_of_action": "Coordinate inter-college programs and ensure project execution timelines are publicly tracked.",
        "council": "CSC",
        "created_at": "2026-03-08",
    },
    {
        "id": "cassc-alyssa-rivera",
        "name": "Alyssa Rivera",
        "position": "President",
        "photo": "images/default-candidate.svg",
        "credentials": "Dean's Lister\nResearch Conference Presenter\nDepartment Organization Officer",
        "plan_of_action": "Advance arts and science student services, research support systems, and transparent policy communication.",
        "council": "CASSC",
        "created_at": "2026-03-08",
    },
    {
        "id": "cbasc-ian-delacruz",
        "name": "Ian Dela Cruz",
        "position": "President",
        "photo": "images/default-candidate.svg",
        "credentials": "Business Pitch Champion\nStudent Entrepreneur Network Officer\nInternship Ambassador",
        "plan_of_action": "Expand internship pipelines, entrepreneurship support, and practical business development opportunities.",
        "council": "CBASC",
        "created_at": "2026-03-08",
    },
    {
        "id": "cfadsc-luna-marquez",
        "name": "Luna Marquez",
        "position": "President",
        "photo": "images/default-candidate.svg",
        "credentials": "Design Competition Finalist\nStudio Organization Coordinator\nCreative Project Lead",
        "plan_of_action": "Strengthen studio resource access, showcase student creatives, and protect student welfare in production-heavy programs.",
        "council": "CFADSC",
        "created_at": "2026-03-08",
    },
]


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "nagkakaisang-tugon-dev-secret")
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 31536000  # 1 year for static files


@app.after_request
def set_cache_headers(response: Any) -> Any:
    """Set cache headers for static and dynamic content."""
    if request.path.startswith("/static/"):
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    else:
        response.headers["Cache-Control"] = "public, max-age=3600"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response


def ensure_storage() -> None:
    DATA_DIR.mkdir(exist_ok=True)

    if not CANDIDATES_FILE.exists():
        CANDIDATES_FILE.write_text("[]", encoding="utf-8")

    if not MESSAGES_FILE.exists():
        MESSAGES_FILE.write_text("[]", encoding="utf-8")


def read_json(file_path: Path) -> list[dict[str, Any]]:
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_json(file_path: Path, payload: list[dict[str, Any]]) -> None:
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)


def load_candidates() -> list[dict[str, Any]]:
    return normalize_candidates(read_json(CANDIDATES_FILE))


def save_candidates(candidates: list[dict[str, Any]]) -> None:
    write_json(CANDIDATES_FILE, normalize_candidates(candidates))


def load_messages() -> list[dict[str, Any]]:
    return read_json(MESSAGES_FILE)


def save_messages(messages: list[dict[str, Any]]) -> None:
    write_json(MESSAGES_FILE, messages)


def normalize_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []

    for item in candidates:
        plan_of_action = item.get("plan_of_action") or item.get("plan") or ""
        council_code = (item.get("council") or "COESC").upper()

        if council_code not in COUNCIL_BY_CODE:
            council_code = "COESC"

        normalized_item = {
            **item,
            "plan_of_action": plan_of_action,
            "council": council_code,
            "created_at": item.get("created_at") or "2026-03-08",
            "photo": item.get("photo") or "images/default-candidate.svg",
        }

        if "plan" in normalized_item:
            del normalized_item["plan"]

        normalized.append(normalized_item)

    existing_ids = {candidate.get("id") for candidate in normalized}
    for seed_candidate in SEED_MULTI_COUNCIL_CANDIDATES:
        if seed_candidate["id"] not in existing_ids:
            normalized.append(seed_candidate)

    return normalized


def candidates_by_council(candidates: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {c["code"]: [] for c in COUNCILS}
    for candidate in candidates:
        grouped.setdefault(candidate["council"], []).append(candidate)
    return grouped


def candidate_short_credentials(candidate: dict[str, Any]) -> str:
    raw = (candidate.get("credentials") or "").splitlines()
    lines = [line.strip() for line in raw if line.strip()]
    return " | ".join(lines[:2]) if lines else "No credentials listed yet."


def get_gallery_items() -> list[dict[str, str]]:
    return [
        {"file": "images/true-through-banner.jpg", "caption": "Alliance campaign banner"},
        {"file": "images/GERONIMO.jpg", "caption": "Campaign trail: candidate engagement"},
        {"file": "images/DELA CRUZ.jpg", "caption": "Council consultation session"},
        {"file": "images/SANIANO.jpg", "caption": "Student outreach and listening forum"},
        {"file": "images/CAMACHO.jpg", "caption": "Alliance leadership and media briefing"},
    ]


@app.context_processor
def inject_navigation_context() -> dict[str, Any]:
    return {
        "councils": COUNCILS,
        "year": 2026,
    }


@app.route("/")
def home() -> str:
    candidates = load_candidates()
    grouped_candidates = candidates_by_council(candidates)
    spotlight_candidates: list[dict[str, Any]] = []

    for council in COUNCILS:
        council_candidates = grouped_candidates.get(council["code"], [])
        if council_candidates:
            spotlight_candidates.append(council_candidates[0])

    platform_sections = [
        {
            "title": "Student Welfare",
            "description": "Accessible support systems, transparent student funds, and responsive representation for day-to-day concerns.",
            "icon": "bi-heart-pulse",
        },
        {
            "title": "Academic Excellence",
            "description": "Peer mentoring, review circles, and evidence-based policies for equitable learning outcomes.",
            "icon": "bi-journal-check",
        },
        {
            "title": "Innovation and Technology",
            "description": "Hands-on innovation projects, digital services, and university-linked technology opportunities.",
            "icon": "bi-cpu",
        },
        {
            "title": "Leadership Development",
            "description": "Leadership tracks, student training, and capacity building across all councils.",
            "icon": "bi-person-badge",
        },
        {
            "title": "Community Engagement",
            "description": "Programs connecting student councils with service initiatives and campus partnerships.",
            "icon": "bi-people",
        },
    ]

    council_cards = [
        {
            "name": council["name"],
            "short_name": council["short_name"],
            "description": council["description"],
            "url": url_for("council_page", slug=council["slug"]),
            "count": len(grouped_candidates.get(council["code"], [])),
        }
        for council in COUNCILS
    ]

    return render_template(
        "index.html",
        spotlight_candidates=spotlight_candidates,
        council_cards=council_cards,
        platform_sections=platform_sections,
        election_day=str(date(2026, 5, 15)),
        gallery_items=get_gallery_items()[:3],
    )


@app.route("/candidates")
def candidates() -> str:
    query = request.args.get("q", "").strip().lower()
    selected_council = request.args.get("council", "ALL").upper()

    all_candidates = load_candidates()
    filtered = all_candidates

    if selected_council != "ALL" and selected_council in COUNCIL_BY_CODE:
        filtered = [item for item in filtered if item["council"] == selected_council]

    if query:
        filtered = [
            item
            for item in filtered
            if query in item.get("name", "").lower() or query in item.get("position", "").lower()
        ]

    for candidate in filtered:
        candidate["short_credentials"] = candidate_short_credentials(candidate)

    return render_template(
        "candidates.html",
        candidates=filtered,
        councils=COUNCILS,
        selected_council=selected_council,
        search_query=request.args.get("q", ""),
    )


@app.route("/candidate/<candidate_id>")
def candidate_profile(candidate_id: str) -> str:
    all_candidates = load_candidates()
    candidate = next((item for item in all_candidates if item.get("id") == candidate_id), None)

    if not candidate:
        flash("Candidate profile not found.", "warning")
        return redirect(url_for("candidates"))

    council = COUNCIL_BY_CODE[candidate["council"]]
    return render_template("candidate_profile.html", candidate=candidate, council=council)


@app.route("/council/<slug>")
def council_page(slug: str) -> str:
    council = COUNCIL_BY_SLUG.get(slug)
    if not council:
        flash("Council page not found.", "warning")
        return redirect(url_for("home"))

    all_candidates = load_candidates()
    council_candidates = [item for item in all_candidates if item["council"] == council["code"]]

    for candidate in council_candidates:
        candidate["short_credentials"] = candidate_short_credentials(candidate)

    return render_template(
        "council.html",
        council=council,
        candidates=council_candidates,
    )


@app.route("/platform")
def platform() -> str:
    sections = [
        {
            "title": "Student Welfare",
            "icon": "bi-heart-pulse",
            "description": "Accessible support systems, responsive case handling, and welfare-first student governance.",
        },
        {
            "title": "Academic Excellence",
            "icon": "bi-journal-check",
            "description": "Peer-led academic support, mentoring networks, and policy advocacy for learning quality.",
        },
        {
            "title": "Innovation and Technology",
            "icon": "bi-cpu",
            "description": "Digitalization projects and innovation initiatives connecting students to modern tools.",
        },
        {
            "title": "Leadership Development",
            "icon": "bi-person-badge",
            "description": "Leadership training and student capacity-building programs across all councils.",
        },
        {
            "title": "Community Engagement",
            "icon": "bi-people",
            "description": "Service programs and participatory governance anchored in student consultation.",
        },
    ]

    return render_template("platform.html", sections=sections)


@app.route("/about")
def about() -> str:
    return render_template("about.html")


@app.route("/contact")
def contact() -> str:
    return render_template("contact.html")


@app.route("/gallery")
def gallery() -> str:
    return render_template("gallery.html", gallery_items=get_gallery_items())


if __name__ == "__main__":
    ensure_storage()
    app.run(debug=True)


ensure_storage()