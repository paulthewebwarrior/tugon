from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from flask import Flask, flash, redirect, render_template, request, url_for


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CANDIDATES_FILE = DATA_DIR / "candidates.json"
MESSAGES_FILE = DATA_DIR / "messages.json"


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "nagkakaisang-tugon-dev-secret")


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
    return read_json(CANDIDATES_FILE)


def save_candidates(candidates: list[dict[str, Any]]) -> None:
    write_json(CANDIDATES_FILE, candidates)


def load_messages() -> list[dict[str, Any]]:
    return read_json(MESSAGES_FILE)


def save_messages(messages: list[dict[str, Any]]) -> None:
    write_json(MESSAGES_FILE, messages)


@app.context_processor
def inject_navigation_context() -> dict[str, Any]:
    candidates = load_candidates()
    return {
        "nav_candidates": candidates,
        "year": 2026,
    }


@app.route("/")
def home() -> str:
    candidates = load_candidates()
    featured_candidates = candidates[:3]
    platform_sections = [
        {
            "title": "Student Welfare",
            "description": "Accessible support systems, transparent student funds, and responsive representation for day-to-day concerns.",
            "icon": "bi-heart-pulse",
        },
        {
            "title": "Academic Support",
            "description": "Peer mentoring, exam review circles, and stronger coordination with faculty for fair and effective learning.",
            "icon": "bi-journal-check",
        },
        {
            "title": "Engineering Innovation",
            "description": "Hands-on design initiatives, project showcases, and industry-linked opportunities that build practical skills.",
            "icon": "bi-cpu",
        },
        {
            "title": "Community Engagement",
            "description": "Programs that connect engineering students to service, leadership, and meaningful campus collaboration.",
            "icon": "bi-people",
        },
    ]
    return render_template(
        "index.html",
        featured_candidates=featured_candidates,
        platform_sections=platform_sections,
    )


@app.route("/candidates")
def candidates() -> str:
    return render_template("candidates.html", candidates=load_candidates())


@app.route("/platform")
def platform() -> str:
    return render_template("platform.html")


@app.route("/about")
def about() -> str:
    return render_template("about.html")


@app.route("/contact")
def contact() -> str:
    return render_template("contact.html")


if __name__ == "__main__":
    ensure_storage()
    app.run(debug=True)


ensure_storage()