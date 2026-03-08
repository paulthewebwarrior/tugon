from __future__ import annotations

import os
import re
from datetime import date
from pathlib import Path
from typing import Any

from flask import Flask, flash, redirect, render_template, request, url_for

import database


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


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
            {
                "title": "ENSC Seminars",
                "icon": "bi-mic",
                "description": "Leadership and professional development seminars for engineering students.",
                "items": [
                    "WomENgineers: Breaking Stigmas - a leadership and professional development seminar on inclusivity, diversity, and empowerment, featuring guest speakers and a panel discussion.",
                    "AIgnite: The Future of Artificial Intelligence - responsible and effective AI use for productivity, engineering tasks, and learning, with emphasis on ethics, limits, and human critical thinking.",
                    "LikhaEN: Mastering Your Thesis Journey - hands-on guidance on topic selection, research methodology, data analysis, and thesis presentation.",
                    "COEmpute with Ease: Calculator Techniques Seminar - practical calculator methods for engineering and scientific problem-solving, computation, and data analysis.",
                    "ENSC General Assembly - a community-building event for freshmen with games, prizes, and introductions to administrators and RSOs.",
                ],
            },
            {
                "title": "Competitive Events",
                "icon": "bi-trophy",
                "description": "Inter-organization competitions that build school spirit and camaraderie.",
                "items": [
                    "ENKabogable: Built Different - RSO competition with formal attire, organization representation, and themed showcases including promotional videos.",
                    "ENScares - Halloween-themed escape room with scheduled group slots, puzzle challenges, and walk-in replacement if groups are late.",
                    "ENtramurals: Sports and Esports Tournament - competitions in Mobile Legends, Valorant, Tekken 8 or Call of Duty: Mobile, basketball, volleyball, badminton, chess, dama, darts, and scrabble (subject to UElympics 2027 alignment).",
                ],
            },
            {
                "title": "Outreach Programs",
                "icon": "bi-heart",
                "description": "Community support initiatives focused on compassion and service.",
                "items": [
                    "ENPaws: Feed and Care - in partnership with Youth for Animals to support humane treatment and organized feeding for resident campus cats.",
                    "ENReach - holiday outreach program for children through gifts, toys, and essential goods for underprivileged communities.",
                ],
            },
            {
                "title": "Student Initiatives",
                "icon": "bi-megaphone",
                "description": "Council-led projects to improve communication, facilities, and daily student experience.",
                "items": [
                    "CENGkonek - semester-end interactive booth with kamustahan sessions for feedback, concerns, and suggestions.",
                    "OpEN Line - anonymous drop box channel for student concerns and suggestions, reviewed monthly.",
                    "ENlocked - additional secure and accessible student lockers.",
                    "ENsights Corner - start-of-year welcome booth for guidance, questions, and council information.",
                    "CENGspection - end-of-semester facility inspections and maintenance coordination with updates.",
                    "ENPARK - clearer parking sticker policy with motorcycle-priority allocation and first-come distribution.",
                    "CENGtuary (SeatEN) - additional benches, chairs, and tables for studying, collaboration, and rest.",
                ],
            },
            {
                "title": "Year-Long Events",
                "icon": "bi-calendar3",
                "description": "Continuous programs that run throughout the academic year.",
                "items": [
                    "ENrinig Ka - monthly online concern and suggestion form with transparency updates on actions taken.",
                    "ENsync - semester-based committee member rotation with open applications for new and returning members.",
                    "CENGspiration - year-long recognition of exemplary engineering students on official social pages.",
                    "ENSCareer Uplifters - cross-disciplinary technical events that generate portfolio-grade outputs for resumes.",
                    "NaENtindihan ka - anonymous expression boxes with optional referral support to Guidance or Student Affairs.",
                ],
            },
            {
                "title": "ACADEMS",
                "icon": "bi-journal-text",
                "description": "Academic Assistance through Distribution of Course Transcriptions.",
                "items": [
                    "Provides organized engineering, mathematics, and science transcriptions for prelims, midterms, and finals.",
                    "Includes voluntary online study sessions and study groups led by year representatives or student volunteers.",
                    "Sessions are recorded to help students review lessons and improve performance.",
                ],
            },
            {
                "title": "Advocacies",
                "icon": "bi-shield-check",
                "description": "Priority advocacy programs for wellness, transparency, and competency growth.",
                "items": [
                    "ENvision Wellness Week - Mental Health Awareness Month activities including seminars, workshops, film showings, and wellness sessions.",
                    "TransparENcy - regular online financial disclosures covering budget allocation, expenses, savings, and sponsors.",
                    "EN-Gauge Competency Mapping - yearly skills roadmap and self-diagnostic reality check aligned with industry expectations.",
                ],
            },
            {
                "title": "Extra Curricular",
                "icon": "bi-people-fill",
                "description": "Programs that strengthen community beyond the classroom.",
                "items": [
                    "ENgageering - team-building event that randomly groups students across courses and year levels for collaborative challenge activities.",
                ],
            },
            {
                "title": "Tangible Projects",
                "icon": "bi-box-seam",
                "description": "Infrastructure and resource projects with visible campus impact.",
                "items": [
                    "Project VENdoExtend - adds vending machines on both sides of the third floor with sanitary napkins, wipes, and tissues.",
                ],
            },
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
    """Ensure database is initialized."""
    DATA_DIR.mkdir(exist_ok=True)
    # Database initialization is handled by the database module on import


def load_candidates() -> list[dict[str, Any]]:
    """Load all candidates from SQLite database."""
    return normalize_candidates(database.load_candidates())


def save_candidates(candidates: list[dict[str, Any]]) -> None:
    """Save candidates to SQLite database."""
    database.save_candidates(normalize_candidates(candidates))


def load_messages() -> list[dict[str, Any]]:
    """Load all messages from SQLite database."""
    return database.load_messages()


def save_message(message: dict[str, Any]) -> None:
    """Save a single message to SQLite database."""
    database.save_message(message)


def normalize_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for index, item in enumerate(candidates, start=1):
        name = str(item.get("name") or "").strip()
        position = str(item.get("position") or "").strip()
        tagline = str(item.get("tagline") or "").strip()
        credentials = str(item.get("credentials") or "").strip()
        plan_of_action = str(item.get("plan_of_action") or item.get("plan") or "").strip()
        brief_introduction = str(item.get("brief_introduction") or item.get("bio") or plan_of_action).strip()
        council_code = str(item.get("council") or "COESC").upper().strip()

        if council_code not in COUNCIL_BY_CODE:
            council_code = "COESC"

        base_id = str(item.get("id") or "").strip()
        if not base_id:
            slug_seed = f"{name}-{position}".lower().strip("-")
            base_id = re.sub(r"[^a-z0-9]+", "-", slug_seed).strip("-") or f"candidate-{index}"

        candidate_id = base_id
        suffix = 2
        while candidate_id in seen_ids:
            candidate_id = f"{base_id}-{suffix}"
            suffix += 1
        seen_ids.add(candidate_id)

        normalized_item = {
            **item,
            "id": candidate_id,
            "name": name,
            "position": position,
            "tagline": tagline,
            "credentials": credentials,
            "plan_of_action": plan_of_action,
            "brief_introduction": brief_introduction,
            "council": council_code,
            "created_at": item.get("created_at") or "2026-03-08",
            "photo": item.get("photo") or "images/default-candidate.svg",
        }

        if "plan" in normalized_item:
            del normalized_item["plan"]

        normalized.append(normalized_item)

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
        election_day=str(date(2026, 3, 25)),
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
    return render_template("platform.html", councils=COUNCILS)


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