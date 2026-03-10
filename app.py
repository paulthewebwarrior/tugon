from __future__ import annotations

import os
import re
from datetime import date
from pathlib import Path
from typing import Any

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for

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
        "positions": [
            "President",
            "Vice President",
            "Secretary",
            "Treasurer",
            "Auditor",
            "PRO",
        ],
        "gpoa": [
            {
                "title": "Academic Programs",
                "icon": "bi-journal-check",
                "description": "Academic policy feedback loops and student consultation forums.",
            },
            {
                "title": "Student Welfare",
                "icon": "bi-heart-pulse",
                "description": "Campus-wide welfare desks, referral systems, and emergency support channels.",
            },
            {
                "title": "Facilities Improvement",
                "icon": "bi-building-check",
                "description": "Cross-college facility audits and student-priority improvement endorsements.",
            },
            {
                "title": "Student Representation",
                "icon": "bi-people",
                "description": "Regular assemblies and transparent policy updates for all colleges.",
            },
            {
                "title": "Innovation and Development",
                "icon": "bi-lightbulb",
                "description": "Digital student services and data-driven governance initiatives.",
            },
        ],
    },
    {
        "code": "ENSC",
        "slug": "engineering",
        "name": "College of Engineering Student Council",
        "short_name": "ENSC",
        "description": "Engineering-focused council promoting technical growth, welfare, and transparent governance.",
        "positions": [
            "President",
            "Vice President",
            "Secretary",
            "Treasurer",
            "Auditor",
            "PRO",
        ],
        "gpoa": [
            {
                "title": "WomENgineers: Breaking Stigmas",
                "icon": "bi-gender-equality",
                "description": "A leadership and professional development seminar focusing on women inclusivity, diversity, and empowerment in the engineering field, featuring guest speakers and a panel discussion.",
            },
            {
                "title": "AIgnite: The Future of Artificial Intelligence",
                "icon": "bi-cpu",
                "description": "This AI seminar teaches students how to use Artificial Intelligence responsibly and effectively. It highlights AI as a tool to enhance productivity, assist in engineering tasks, and support learning, while emphasizing ethical use, limitations, and the irreplaceable role of human creativity and critical thinking in the profession.",
            },
            {
                "title": "LikhaEN: Mastering Your Thesis Journey",
                "icon": "bi-file-earmark-text",
                "description": "A hands-on seminar designed to guide students through the process of crafting a successful thesis. The workshop covers essential skills such as topic selection, research methodology, data analysis, and effective presentation techniques.",
            },
            {
                "title": "COEmpute with Ease: Calculator Techniques Seminar",
                "icon": "bi-calculator",
                "description": "CalTech offers a hands-on seminar on advanced calculator techniques for engineering and scientific applications. Participants will learn efficient methods for problem-solving, data analysis, and computation, enhancing their accuracy, speed, and confidence in tackling complex academic tasks.",
            },
            {
                "title": "ENlink",
                "icon": "bi-people",
                "description": "The College of Engineering General Assembly is a fun and engaging community-building event, primarily for freshmen. Through games, prizes, and interactive activities, students bond with peers while getting introduced to the College administrators and the various RSOs they can join.",
            },
            {
                "title": "ENrights, ENvironment",
                "icon": "bi-book",
                "description": "This educational seminar is a comprehensive initiative designed to talk about student rights and their capabilities within the university. Beyond rights, the seminar also addresses how they take care of their environment as students.",
            },
            {
                "title": "ENKabogable: Built Different",
                "icon": "bi-award",
                "description": "The event is a competition among different RSOs featuring several categories such as formal attire, organization representation, and the chosen theme. Candidates will present promotional videos showcasing their respective organizations.",
            },
            {
                "title": "ENScares",
                "icon": "bi-door-open",
                "description": "An escape room where students can register in groups, with the option to schedule their time slot in advance. The escape room will feature various obstacles such as puzzles, problem-solving challenges, and jump scares to match the Halloween theme.",
            },
            {
                "title": "ENtramurals: Sports and Esports Tournament",
                "icon": "bi-controller",
                "description": "A vibrant celebration of teamwork, strategy, and sportsmanship. For Esports: Mobile Legends, Valorant, and Tekken 8/Call of Duty: Mobile. For Sports: Basketball, Volleyball, Badminton, Chess, Dama, Darts, and Scrabble. Note: Games vary depending on UElympics 2027.",
            },
            {
                "title": "ENgageering",
                "icon": "bi-person-plus",
                "description": "A team-building event for Engineering students that promotes teamwork, unity, and new connections. Students from different courses and year levels will be randomly grouped to complete activity challenges.",
            },
            {
                "title": "ENPaws: Feed and Care",
                "icon": "bi-heart",
                "description": "In partnership with Youth for Animals (YFA), this outreach supports the feeding and care of resident cats at the University of the East. It promotes humane treatment, organized feeding, and a culture of compassion within the campus community.",
            },
            {
                "title": "ENReach",
                "icon": "bi-gift",
                "description": "An outreach program that focuses on giving children gifts, toys, and goods during the holiday season. A consistent tradition showing care for the underprivileged.",
            },
            {
                "title": "CENGkonek",
                "icon": "bi-chat-dots",
                "description": "Semester-end interactive booth for Engineering students featuring kamustahan sessions - creating an open space for sharing experiences, concerns, feedback, and suggestions.",
            },
            {
                "title": "OpEN Line",
                "icon": "bi-inbox",
                "description": "Anonymous drop box for students to submit concerns, feedback, and suggestions - an official physical channel for voicing ideas about the council, college, and university. Responses are monitored monthly.",
            },
            {
                "title": "ENsights Corner",
                "icon": "bi-question-circle",
                "description": "Start-of-year welcome booth for Engineering students - a friendly space to ask questions, seek assistance, and learn about the council's programs and services.",
            },
            {
                "title": "CENGspection",
                "icon": "bi-clipboard-check",
                "description": "End-of-semester checklist-based inspections of Engineering college facilities, coordinates with maintenance to resolve issues, accepts student reports, and provides updates for safe, functional learning environments.",
            },
            {
                "title": "ENPARK",
                "icon": "bi-p-square",
                "description": "Aims to improve the parking system for Engineering students by creating a clear policy for the distribution of parking stickers. Sticker prices will be lower for motorcycles than for cars.",
            },
            {
                "title": "CENGtuary (SeatEN)",
                "icon": "bi-bench",
                "description": "An initiative project aimed at enhancing student comfort and productivity within the college. Through this project, benches, chairs, and tables will be strategically placed in the Engineering building and other open spaces.",
            },
            {
                "title": "ENvision Wellness Week",
                "icon": "bi-heart-pulse",
                "description": "A week-long event in October for Mental Health Awareness Month featuring seminars, workshops, film showings, and wellness activities. It promotes mental well-being, reduces stigma, and encourages self-care through mindfulness and stress-management sessions.",
            },
            {
                "title": "ENsync",
                "icon": "bi-arrow-repeat",
                "description": "The ENSC Committee implements a semester-based member rotation system, offering open applications each term for both new students eager to contribute and returning members wishing to continue their service.",
            },
            {
                "title": "CENGspiration",
                "icon": "bi-star",
                "description": "This year-long event spotlights exemplary College of Engineering students - including student leaders, competition winners, and others who demonstrate outstanding ability - by featuring them on our Facebook Page as role models.",
            },
            {
                "title": "ENSCareer Uplifters",
                "icon": "bi-briefcase",
                "description": "Series of events that bridge the gap between academic theory and industry hiring standards. The Student Council, in collaboration with RSOs, will implement a series of high-impact, cross-disciplinary technical events.",
            },
            {
                "title": "NaENtindihan ka",
                "icon": "bi-emoji-smile",
                "description": "This year-long initiative provides designated boxes where students can write and share their feelings. They may submit notes anonymously or include their student number if they want the council to help connect them with the Guidance Office.",
            },
            {
                "title": "ACADEMS",
                "icon": "bi-journal-text",
                "description": "Academic Assistance through Distribution of Course Transcriptions (ACADEMS) is a student-led initiative providing organized transcriptions of Engineering, Mathematics, and Science courses for prelims, midterms, and finals.",
            },
            {
                "title": "ENlocked",
                "icon": "bi-lock",
                "description": "Council-led project providing additional secure, accessible lockers to ease students' concerns about personal belongings.",
            },
            {
                "title": "ENrinig Ka",
                "icon": "bi-chat-square",
                "description": "This year-long initiative provides students with a platform to submit their concerns, suggestions, and feedback to the council, administration, or facilities through an online form.",
            },
            {
                "title": "TransparENcy",
                "icon": "bi-graph-up",
                "description": "This advocacy promotes open communication, honesty, and accountability. Updates on facility inspections will be regularly posted. Financial reports including budget allocation, expenses, remaining balance, and sponsors will be shared online.",
            },
            {
                "title": "NO TO TOFI",
                "icon": "bi-x-circle",
                "description": "Scholarship Quota advocacy.",
            },
            {
                "title": "EN-Gauge - Competency Mapping",
                "icon": "bi-signpost-split",
                "description": "The Student Council will publish a Yearly Skills Roadmap that clearly lists the specific technical and soft skills students should focus on at each year level to stay job-ready.",
            },
            {
                "title": "PROJECT VENdoExtend",
                "icon": "bi-cart",
                "description": "Aims to provide easier access to essential hygiene products for students. This project plans to add vending machines on both sides of the 3rd floor with sanitary napkins, wipes, and tissues.",
            },
        ],
    },
    {
        "code": "CASSC",
        "slug": "arts_science",
        "name": "College of Arts and Science Student Council",
        "short_name": "CASSC",
        "description": "Council for liberal arts and sciences centered on inclusive representation and interdisciplinary growth.",
        "positions": [
            "President",
            "Vice President",
            "Secretary",
            "Treasurer",
            "Auditor",
            "PRO",
        ],
        "gpoa": [
            {
                "title": "CAS Anchor: Navigate. Connect. Thrive.",
                "icon": "bi-discord",
                "description": "A digital support platform hosted through an official Discord server that provides CAS students with academic resources, campus guides, departmental information, and a real-time 'Ask-a-Senior' channel.",
                "items": [
                    "Academic resources and campus guides",
                    "Departmental information database",
                    "Real-time 'Ask-a-Senior' channel for academic and campus concerns",
                ],
            },
            {
                "title": "UE-CAS Knowledge Network",
                "icon": "bi-book",
                "description": "A centralized e-library and digital archive for CAS students to store and access research papers, essays, term papers, case studies, and creative works.",
            },
            {
                "title": "CASalindunghan: Pagdiriwang ng Buwan ng Wika",
                "icon": "bi-flag",
                "description": "A celebration of Filipino culture and language through traditional Filipino games, a Filipino Sign Language seminar, and a Baybayin workshop.",
            },
            {
                "title": "Ang Buhay ay Hindi CAREERa!",
                "icon": "bi-briefcase",
                "description": "A career guidance seminar featuring CAS alumni who share their post-graduation experiences and career journeys.",
            },
            {
                "title": "Ihataw Mo CASmate!",
                "icon": "bi-music-note-beamed",
                "description": "Free dance sessions for CAS students promoting creativity, physical wellness, and stress relief.",
            },
            {
                "title": "CAS of Heart",
                "icon": "bi-heart",
                "description": "Valentine-themed activity with bracelet-making, love letter writing, and a Freedom Wall for positive messages.",
            },
            {
                "title": "Mr. and Ms. CASambassador",
                "icon": "bi-camera",
                "description": "Digital ambassador program where CAS students create promotional content for partner sponsors.",
            },
            {
                "title": "CAS EmpowHERment Month",
                "icon": "bi-gender-equality",
                "description": "Month-long program celebrating National Women's Month with women's rights, empowerment, mental health, and wellness activities.",
            },
            {
                "title": "CAS Debate Contest",
                "icon": "bi-chat-square-quote",
                "description": "Structured debate competition for CAS students on political, social, scientific, and cultural topics.",
            },
            {
                "title": "CAS Learning Space Improvement",
                "icon": "bi-layout-text-window-reverse",
                "description": "Enhancing the CAS learning area with additional seating, mats, and table coverings.",
            },
            {
                "title": "CASecure Lockers (CAS Lockers 2.0)",
                "icon": "bi-lock",
                "description": "Additional locker facilities for CAS students with an official rental system coordinated with Student Affairs.",
            },
            {
                "title": "CAS Connect: Stay Connected and Recharged",
                "icon": "bi-wifi",
                "description": "Student support project for borrowing pocket Wi-Fi devices and extension wires.",
            },
            {
                "title": "CASchedules: Information Board",
                "icon": "bi-calendar-check",
                "description": "Monthly updated bulletin board displaying important announcements and events for CAS students.",
            },
            {
                "title": "CASiyahan sa Silangan: Welcoming Party",
                "icon": "bi-balloon",
                "description": "Annual welcoming celebration for CAS students with games, performances, and organization introductions.",
            },
            {
                "title": "CASabay, CASkwela!: CAS Welcoming Week",
                "icon": "bi-people",
                "description": "Week-long initiative with student help desk, CASINEMA movie bonding, and CASyoso student marketplace.",
            },
            {
                "title": "CASportsfest: Tagisan ng LaCAS!",
                "icon": "bi-trophy",
                "description": "Multi-week sports competition showcasing talents in physical sports and e-sports.",
            },
            {
                "title": "CASquerade Ball",
                "icon": "bi-mask",
                "description": "Formal culminating event celebrating achievements with performances, awards, and social activities.",
            },
            {
                "title": "ShowCASing: On the Record",
                "icon": "bi-bar-chart",
                "description": "Transparency initiative presenting financial reports and sponsorship records through creative infographics.",
            },
            {
                "title": "CASulatan",
                "icon": "bi-chat-dots",
                "description": "Online feedback platform for CAS students to submit questions, concerns, and suggestions.",
            },
            {
                "title": "CASrangalan",
                "icon": "bi-award",
                "description": "Semester recognition program honoring CAS student organizations for outstanding performance.",
            },
            {
                "title": "CAS Gazette",
                "icon": "bi-newspaper",
                "description": "Student information publication highlighting campus updates and council activities.",
            },
            {
                "title": "CASani-Check Dashboard",
                "icon": "bi-qr-code",
                "description": "Sanitation monitoring system allowing students to report restroom concerns via QR codes.",
            },
            {
                "title": "CASama: Mental Health Week",
                "icon": "bi-heart-pulse",
                "description": "Week-long mental wellness program with art therapy, seminars, and group healing activities.",
            },
            {
                "title": "The CAS Plate: Taste & Rate",
                "icon": "bi-cup-hot",
                "description": "Culinary showcase by Hospitality Management students with pop-up food booths and rating system.",
            },
            {
                "title": "SafeCASe: Firearm Safety and Disarming Skills",
                "icon": "bi-shield-exclamation",
                "description": "Educational seminar on firearm safety, regulations, and basic disarming demonstrations.",
            },
            {
                "title": "CASkybound: Cabin Crew Preparatory Workshop",
                "icon": "bi-airplane",
                "description": "Professional training workshop for Tourism students on grooming, safety, and situational handling.",
            },
            {
                "title": "Filters and Frames: Turuan Mo Ako, CommATE!",
                "icon": "bi-camera2",
                "description": "Multimedia workshop teaching photography, videography, and filmmaking fundamentals.",
            },
        ],
    },
    {
        "code": "CBASC",
        "slug": "business_admin",
        "name": "College of Business and Administration Student Council",
        "short_name": "CBASC",
        "description": "Business council promoting leadership, entrepreneurship, and student-centered services.",
        "positions": [
            "President",
            "Vice President",
            "Secretary",
            "Treasurer",
            "Auditor",
            "PRO",
        ],
        "gpoa": [
            {
                "title": "Academic Programs",
                "icon": "bi-briefcase",
                "description": "Certification support, case competitions, and internship readiness.",
            },
            {
                "title": "Student Welfare",
                "icon": "bi-heart-pulse",
                "description": "Accessible welfare systems tailored to business student concerns.",
            },
            {
                "title": "Facilities Improvement",
                "icon": "bi-building-check",
                "description": "Learning hub upgrades and resource center improvements.",
            },
            {
                "title": "Student Representation",
                "icon": "bi-people",
                "description": "Open consultation mechanisms for policy and event planning.",
            },
            {
                "title": "Innovation and Development",
                "icon": "bi-graph-up-arrow",
                "description": "Entrepreneurship labs and startup-oriented learning initiatives.",
            },
        ],
    },
    {
        "code": "CFADSC",
        "slug": "fine_arts",
        "name": "College of Fine Arts, Architecture and Design Student Council",
        "short_name": "CFADSC",
        "description": "Creative council championing design excellence, student welfare, and collaborative culture.",
        "positions": [
            "President",
            "Vice President",
            "Secretary",
            "Treasurer",
            "Auditor",
            "PRO",
        ],
        "gpoa": [
            {
                "title": "Academic Programs",
                "icon": "bi-pencil-square",
                "description": "Critique sessions, portfolio development, and professional design coaching.",
            },
            {
                "title": "Student Welfare",
                "icon": "bi-heart",
                "description": "Student support systems balancing studio life and wellness.",
            },
            {
                "title": "Facilities Improvement",
                "icon": "bi-house-gear",
                "description": "Studio upgrades and better access to design resources and spaces.",
            },
            {
                "title": "Student Representation",
                "icon": "bi-people",
                "description": "Inclusive representation across art, architecture, and design programs.",
            },
            {
                "title": "Innovation and Development",
                "icon": "bi-palette",
                "description": "Creative innovation programs and interdisciplinary project showcases.",
            },
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
        plan_of_action = str(
            item.get("plan_of_action") or item.get("plan") or ""
        ).strip()
        brief_introduction = str(
            item.get("brief_introduction") or item.get("bio") or plan_of_action
        ).strip()
        council_code = str(item.get("council") or "ENSC").upper().strip()

        if council_code not in COUNCIL_BY_CODE:
            council_code = "ENSC"

        base_id = str(item.get("id") or "").strip()
        if not base_id:
            slug_seed = f"{name}-{position}".lower().strip("-")
            base_id = (
                re.sub(r"[^a-z0-9]+", "-", slug_seed).strip("-") or f"candidate-{index}"
            )

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


def candidates_by_council(
    candidates: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {c["code"]: [] for c in COUNCILS}
    for candidate in candidates:
        grouped.setdefault(candidate["council"], []).append(candidate)
    return grouped


def candidate_short_credentials(candidate: dict[str, Any]) -> str:
    raw = (candidate.get("credentials") or "").splitlines()
    lines = [line.strip() for line in raw if line.strip()]
    return " | ".join(lines[:2]) if lines else "No credentials listed yet."


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
            if query in item.get("name", "").lower()
            or query in item.get("position", "").lower()
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
    candidate = next(
        (item for item in all_candidates if item.get("id") == candidate_id), None
    )

    if not candidate:
        flash("Candidate profile not found.", "warning")
        return redirect(url_for("candidates"))

    council = COUNCIL_BY_CODE[candidate["council"]]
    return render_template(
        "candidate_profile.html", candidate=candidate, council=council
    )


@app.route("/council/<slug>")
def council_page(slug: str) -> str:
    council = COUNCIL_BY_SLUG.get(slug)
    if not council:
        flash("Council page not found.", "warning")
        return redirect(url_for("home"))

    all_candidates = load_candidates()
    council_candidates = [
        item for item in all_candidates if item["council"] == council["code"]
    ]

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


# ============== API Endpoints ==============


@app.route("/api/candidates")
def api_candidates() -> Any:
    """API endpoint to get all candidates with optional filtering."""
    query = request.args.get("q", "").strip().lower()
    council_filter = request.args.get("council", "ALL").upper()

    all_candidates = load_candidates()
    filtered = all_candidates

    if council_filter != "ALL" and council_filter in COUNCIL_BY_CODE:
        filtered = [c for c in filtered if c["council"] == council_filter]

    if query:
        filtered = [
            c
            for c in filtered
            if query in c.get("name", "").lower()
            or query in c.get("position", "").lower()
        ]

    # Add short_credentials to each candidate
    for candidate in filtered:
        candidate["short_credentials"] = candidate_short_credentials(candidate)

    return jsonify({"candidates": filtered, "total": len(filtered)})


@app.route("/api/candidate/<candidate_id>")
def api_candidate(candidate_id: str) -> Any:
    """API endpoint to get a single candidate by ID."""
    all_candidates = load_candidates()
    candidate = next((c for c in all_candidates if c.get("id") == candidate_id), None)

    if not candidate:
        return jsonify({"error": "Candidate not found"}), 404

    candidate["short_credentials"] = candidate_short_credentials(candidate)
    council = COUNCIL_BY_CODE.get(candidate["council"])

    return jsonify({"candidate": candidate, "council": council})


@app.route("/api/councils")
def api_councils() -> Any:
    """API endpoint to get all councils."""
    return jsonify({"councils": COUNCILS})


@app.route("/api/council/<slug>")
def api_council(slug: str) -> Any:
    """API endpoint to get a single council and its candidates."""
    council = COUNCIL_BY_SLUG.get(slug)
    if not council:
        return jsonify({"error": "Council not found"}), 404

    all_candidates = load_candidates()
    council_candidates = [c for c in all_candidates if c["council"] == council["code"]]

    for candidate in council_candidates:
        candidate["short_credentials"] = candidate_short_credentials(candidate)

    return jsonify({"council": council, "candidates": council_candidates})


@app.route("/api/home")
def api_home() -> Any:
    """API endpoint to get home page data."""
    candidates = load_candidates()
    grouped_candidates = candidates_by_council(candidates)
    spotlight_candidates: list[dict[str, Any]] = []

    for council in COUNCILS:
        council_candidates = grouped_candidates.get(council["code"], [])
        if council_candidates:
            candidate = council_candidates[0].copy()
            candidate["short_credentials"] = candidate_short_credentials(candidate)
            spotlight_candidates.append(candidate)

    council_cards = [
        {
            "name": council["name"],
            "short_name": council["short_name"],
            "description": council["description"],
            "slug": council["slug"],
            "count": len(grouped_candidates.get(council["code"], [])),
        }
        for council in COUNCILS
    ]

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

    return jsonify(
        {
            "spotlight_candidates": spotlight_candidates,
            "council_cards": council_cards,
            "platform_sections": platform_sections,
            "election_day": str(date(2026, 3, 25)),
        }
    )


if __name__ == "__main__":
    ensure_storage()
    app.run(debug=True)


ensure_storage()
