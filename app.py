import pandas as pd
# from __future__ import annotations

import os
import re
from datetime import date
from functools import lru_cache
from pathlib import Path
from typing import Any

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for

import database
from database import get_position_order


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


# --- CLI command for table creation (must be after app/db init) ---


COUNCILS: list[dict[str, Any]] = [
    {
        "code": "CSC",
        "heart_img": "images/hearts/yellow.png",
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
                "title": "IGNITING LEADERS; SHAPING WARRIORS",
                "icon": "bi-people",
                "description": "An engaging and interactive leadership seminar for aspiring SHS and College student leaders, featuring carefully selected speakers who will share their leadership experiences, insights, and practical approaches to student leadership.",
            },
            {
                "title": "MANDIRIGMA NG PAGKAKAIBA: Warriors of Diversity",
                "icon": "bi-globe2",
                "description": "A youth-driven advocacy that champions inclusivity and unity in the university. Rooted in the warrior spirit (mandirigma), it calls on students to embrace cultural, social, and personal differences as sources of strength through a series of events and seminars.",
            },
            {
                "title": "UE-DUCATIONAL WARRIORS' DISCUSSION",
                "icon": "bi-chat-dots",
                "description": "An engaging university-wide seminar that serves as a healthy dialogue bridging expert insights and student perspectives on social, political, environmental, and educational issues.",
            },
            {
                "title": "MENTAL HEALTH TALK",
                "icon": "bi-heart-pulse",
                "description": "A seminar focused on mental health awareness, emotional well-being, and providing students with knowledge about self-care practices and available support systems within the university.",
            },
            {
                "title": "Akbay Balikat Program: Warriors with Diverse Abilities",
                "icon": "bi-universal-access",
                "description": "This program empowers and supports the diverse abilities of PWD students through needs-based and talent-focused interventions rather than disability-based categorization.",
            },
            {
                "title": "Mandirigma Study Grounds: Study Areas and Benches",
                "icon": "bi-book",
                "description": "This project provides additional study areas and benches across campus to create a comfortable and conducive environment for learning.",
            },
            {
                "title": "BOOK NOOK",
                "icon": "bi-bookmark",
                "description": "This project maximizes the vacant area outside the library to be transformed into a comfortable and favorable spot for students to spend their leisure time, read, and/or study with less restrictions.",
            },
            {
                "title": "SUPPORT THE UE CHAMPIONS: Students Assistance Program",
                "icon": "bi-trophy",
                "description": "A council-led movement to help students compete outside the university through administrative support, sponsorships, and in-kind contributions, ensuring they represent UE-Caloocan with pride.",
            },
            {
                "title": "PA System in EN Building",
                "icon": "bi-speaker",
                "description": "This project provides a Public Address (PA) system in the EN Building to improve communication and announcements for students and staff.",
            },
            {
                "title": "WIFI BOOSTER",
                "icon": "bi-wifi",
                "description": "WiFi boosters will be requested to improve internet connectivity all over the campus to help students attend online classes without interruptions.",
            },
            {
                "title": "CAPEX",
                "icon": "bi-cash-coin",
                "description": "This petition seeks clarification and reconsideration of the current policy of allocating unutilized Student Council funds to Capital Expenditures (CAPEX).",
            },
            {
                "title": "MANDIRIGMA NG PAG-UNLAD: Warriors for a Functional University",
                "icon": "bi-building",
                "description": "This advocacy seeks to address unfixed, neglected, and lacking facilities in the university, requesting the addition of blinds to every classroom and strengthening the directory in every college.",
            },
            {
                "title": "NO TO TOFI",
                "icon": "bi-x-circle",
                "description": "This action plan campaigns against any increase in tuition and other school fees to protect students from additional financial burden.",
            },
            {
                "title": "7% SCHOLARSHIP QUOTA",
                "icon": "bi-graduation-cap",
                "description": "This project serves as a dedicated advocacy that focuses on reassessing and improving the 7% scholarship quota to better support deserving students.",
            },
            {
                "title": "DIGITAL SURVEY FEEDBACK",
                "icon": "bi-qr-code",
                "description": "QR codes posted around the campus will lead to a Google Form where students can easily submit concerns about the council, administration, faculty members, or facilities.",
            },
            {
                "title": "The Warriors' Trail: The Ultimate UEversity Walk",
                "icon": "bi-signpost-2",
                "description": "Formerly the 'Freshmen Walk', is an enhanced interactive campus tour for all year levels to explore the school and meet fellow students.",
            },
            {
                "title": "UEnited: The General Assembly",
                "icon": "bi-people-fill",
                "description": "This university-wide event will include all grade levels and colleges to gather for a general assembly and a formal welcoming for the new school year.",
            },
            {
                "title": "UE RAVE & LOUD: The Ultimate Campus Concert Experience 2026",
                "icon": "bi-music-note-beamed",
                "description": "A high-energy, rave-concept campus concert showcasing the talent, music, and school spirit of UE-Caloocan students.",
            },
            {
                "title": "ALL EYES ON UE: MIX ECO WARRIORS",
                "icon": "bi-gem",
                "description": "An inclusive, glamorous campus pageant showcasing the talent, charm, and confidence of UE students through outfits made from recyclable or upcycled materials.",
            },
            {
                "title": "UE GOT TALENT",
                "icon": "bi-star",
                "description": "An event and competition designed to showcase a diverse variety of talents from the UE-Caloocan students.",
            },
            {
                "title": "SUSTAINATOPIA 2.0",
                "icon": "bi-shop",
                "description": "A campus bazaar that allows students from different departments to sell their products, such as artworks, crafts, and pre-loved items.",
            },
            {
                "title": "UELYMPICS SPORTSFEST 2027",
                "icon": "bi-controller",
                "description": "A week-long sports festival promoting fitness, teamwork, and school spirit, featuring basketball, volleyball, and badminton tournaments.",
            },
            {
                "title": "ORGANIZATION WEEK",
                "icon": "bi-calendar-event",
                "description": "Organization Week is a week-long campus event designed to highlight the programs, initiatives, and creativity of RSOs and uni-wide organizations.",
            },
            {
                "title": "Cinema ng Mandirigma: Discover Your Future at UE",
                "icon": "bi-film",
                "description": "A campus-wide film screening that provides relaxation, entertainment, and social interaction among students.",
            },
            {
                "title": "EastCast: The Pulse of UE",
                "icon": "bi-mic",
                "description": "This project implements a PA System across the university that will allow students to showcase their broadcasting skills.",
            },
            {
                "title": "WONDER PETS",
                "icon": "bi-heart",
                "description": "A day where Student-Pet Lovers are invited to bring their pets inside the campus for a get-together and a short program.",
            },
            {
                "title": "Warrior Fest: Rides, Pride, and Spirit",
                "icon": "bi-balloon",
                "description": "A campus carnival featuring exciting rides designed to engage students, foster camaraderie, and promote school spirit.",
            },
            {
                "title": "Transparency and Inventory Report",
                "icon": "bi-clipboard-data",
                "description": "This project ensures transparency and accountability in the management of Student Council resources through regular inventory checks and reports.",
            },
            {
                "title": "Bukas sa Silangan: Discover Your Future at UE",
                "icon": "bi-door-open",
                "description": "This project is an Open Campus initiative designed to give future students the opportunity to explore the university.",
            },
            {
                "title": "KAPIT KARAMAY: Calamity Response Initiative",
                "icon": "bi-hand-thumbs-up",
                "description": "Kapit Karamay is a student-led initiative that serves as an immediate and organized assistance to members of the school community affected by calamities.",
            },
            {
                "title": "PUSO NG MANDIRIGMA: Celebrating Family Bonds",
                "icon": "bi-gift",
                "description": "Outreach program that provides grocery packs and essential food items to non-teaching staff to support staff welfare.",
            },
            {
                "title": "MANDIRIGMA SHARE & CARE",
                "icon": "bi-arrow-repeat",
                "description": "A sharing initiative where students can borrow, share, and return essential items such as books, art materials, calculators, and other academic materials.",
            },
            {
                "title": "VOICE FOR PEACE: Supporting Refugee Students",
                "icon": "bi-people",
                "description": "This initiative promotes understanding and support for refugee students, advocating for their rights and inclusion.",
            },
        ],
    },
    {
        "code": "ENSC",
        "heart_img": "images/hearts/orange.png",
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
        "heart_img": "images/hearts/green.png",
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
        "heart_img": "images/hearts/blue.png",
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
                "title": "Beacons Serving BAcon",
                "icon": "bi-people",
                "description": "An interactive seminar featuring alumni and graduating students who will share their experiences regarding coursework, examinations, internships, time management, and college life. The event will conclude with an open forum where students can ask questions and gain practical advice that will guide them throughout their academic and professional journeys.",
            },
            {
                "title": "BAlanseng Budget: Financial Literacy Bootcamp",
                "icon": "bi-cash-coin",
                "description": "A financial literacy seminar led by qualified speakers that will discuss practical financial skills such as budgeting, saving, investing, managing allowances or income, understanding debt, and making responsible financial decisions to help students build financial independence.",
            },
            {
                "title": "BAsta Prepared sa BA!: A Finals Review Session",
                "icon": "bi-journal-check",
                "description": "An academic support program conducted every finals week that provides students with guided review sessions on key subjects, helping them prepare effectively for examinations through discussions, shared study resources, and collaboration with Recognized Student Organizations.",
            },
            {
                "title": "BAgong BArkada sa BA",
                "icon": "bi-emoji-smile",
                "description": "A welcoming general assembly and freshman orientation event that aims to introduce new students to the CBA community, allowing them to meet fellow students, faculty members, and student leaders through games, performances, and organization presentations.",
            },
            {
                "title": "BA Market",
                "icon": "bi-shop",
                "description": "A week-long entrepreneurial pop-up fair where student entrepreneurs can promote and sell their products such as handmade goods, apparel, and novelty items, providing them with hands-on experience in marketing, selling, and business operations.",
            },
            {
                "title": "Pasko sa Kahon: Gift-Giving Program",
                "icon": "bi-gift",
                "description": "A Christmas outreach initiative where students prepare gift-filled shoeboxes containing school supplies and essential items for elementary school children, spreading joy and generosity during the holiday season.",
            },
            {
                "title": "The Chamber of Wonders – BA Fest",
                "icon": "bi-stars",
                "description": "A Harry Potter-themed year-end celebration that divides BA courses into different houses for friendly competitions, performances, themed booths, and activities that promote camaraderie, teamwork, and school spirit.",
            },
            {
                "title": "Organization Rooms for CBA RSOs",
                "icon": "bi-building",
                "description": "A relocation initiative that aims to transfer Recognized Student Organization rooms from the Engineering Building to the Tan Yan Kee Building to provide a more secure, accessible, and collaborative working environment for student leaders.",
            },
            {
                "title": "BA Arena: The Ultimate Sports BAttle",
                "icon": "bi-trophy",
                "description": "A college-wide sports competition that features both physical sports such as basketball, volleyball, badminton, and soccer, as well as e-sports tournaments including Mobile Legends, Call of Duty, and Valorant, encouraging teamwork, sportsmanship, and healthy competition.",
            },
            {
                "title": "BAck To Better Locker",
                "icon": "bi-lock",
                "description": "A project aimed at upgrading and replacing damaged lockers with improved and durable storage facilities to ensure students have a safe and reliable place to store their belongings within the campus.",
            },
            {
                "title": "EO’s Cup",
                "icon": "bi-patch-question",
                "description": "A business knowledge quiz competition designed specifically for Executive Officers of CBA Recognized Student Organizations to test their knowledge, teamwork, and strategic thinking through multiple rounds of challenging questions.",
            },
            {
                "title": "BA Consultation: We Got Your BAck!",
                "icon": "bi-chat-dots",
                "description": "A consultation platform where students can anonymously voice concerns regarding academics, facilities, and student welfare, allowing the council to collect feedback and coordinate with college officials to address issues effectively.",
            },
            {
                "title": "The Grand BAll: Going BAyond Limits",
                "icon": "bi-balloon",
                "description": "A formal prom-inspired event where students gather for an elegant evening of dancing, performances, and the coronation of a BA Prom King and Queen, celebrating student confidence, unity, and school pride.",
            },
            {
                "title": "BAhaghari sa Silangan",
                "icon": "bi-rainbow",
                "description": "A Pride Month digital competition featuring poster-making and photography contests that highlight themes of diversity, acceptance, equality, and identity, promoting inclusivity within the CBA community.",
            },
            {
                "title": "Tatak BA: Our Mark Our Pride",
                "icon": "bi-shirt",
                "description": "A college merchandise initiative where students participate in a design contest to create the official CBA shirt, symbolizing unity, pride, and belonging among members of the college.",
            },
            {
                "title": "BAse Camp: Workshop Preparation for the Real World",
                "icon": "bi-briefcase",
                "description": "A career readiness workshop designed for graduating students that focuses on resume building, portfolio preparation, job interview simulations, and professional development to prepare them for employment after graduation.",
            },
            {
                "title": "SaBayan: BAlandra ng Talento",
                "icon": "bi-mic",
                "description": "A talent showcase competition where students can present their abilities in singing, dancing, spoken word, or other performances, encouraging creativity, self-expression, and confidence.",
            },
            {
                "title": "BAgong Hakbang sa UE CBA",
                "icon": "bi-mortarboard",
                "description": "An academic orientation program for senior high school ABM students that introduces them to the courses, opportunities, and career paths offered by the College of Business Administration to encourage future enrollment.",
            },
            {
                "title": "BA-sket of Knowledge",
                "icon": "bi-journal-richtext",
                "description": "A dedicated collaborative learning space designed for BA students where they can study individually or in groups, review lessons, share ideas, and prepare for examinations in a supportive academic environment.",
            },
            {
                "title": "Handa ka na BA?",
                "icon": "bi-question-circle",
                "description": "A general knowledge quiz bee that challenges students’ knowledge in various academic fields such as mathematics, science, history, and geography, promoting intellectual engagement and healthy academic competition.",
            },
        ],
    },
    {
        "code": "CFADSC",
        "heart_img": "images/hearts/red.png",
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
                "title": "ABOT KAMAY 3.0: Paminggalan ng Tulungan",
                "icon": "bi-box-seam",
                "description": "A resource-sharing initiative that collects pre-loved and extra art materials from alumni and students, redistributing them to CFAD students who need creative supplies. The project promotes sustainability, accessibility, and community support by giving unused materials a second life.",
            },
            {
                "title": "MALIKHAING SALAMIN 3.0: Reflecting Truth, Projecting Change",
                "icon": "bi-chat-dots",
                "description": "A hybrid communication platform that enables CFAD students to share feedback, concerns, and suggestions through both digital and face-to-face channels, strengthening transparency and student representation within the council.",
            },
            {
                "title": "TALA-UGNAYAN: Komite Konstelasyon",
                "icon": "bi-star",
                "description": "A leadership development program that engages CFAD students in council-led initiatives, providing hands-on experience in project planning, collaboration, and student governance while nurturing future student leaders.",
            },
            {
                "title": "HIMIG AT HABI: CFAD Artist Alley",
                "icon": "bi-shop",
                "description": "A bimonthly student marketplace where CFAD artists and designers can showcase and sell their creative works through curated themed installations aligned with cultural milestones and global observances.",
            },
            {
                "title": "CFAD-NIMULA: Freshmen Walk and Welcoming Party",
                "icon": "bi-people",
                "description": "A welcoming program for first-year CFAD students featuring a campus tour, parade, and general assembly to help freshmen familiarize themselves with facilities, organizations, and the creative community.",
            },
            {
                "title": "CFADPASKUHAN: Paskong Mapaglikha",
                "icon": "bi-snow",
                "description": "A year-end celebration for the CFAD community that highlights creative collaboration, reflection, and camaraderie through festive activities and artistic presentations.",
            },
            {
                "title": "CFADPluma: Kalipunan ng Kahusayan",
                "icon": "bi-journal-bookmark",
                "description": "An official digital publication and exhibit that archives the achievements, awards, and milestones of CFAD students and alumni, culminating in a recognition program celebrating excellence in the arts and design.",
            },
            {
                "title": "Sa Muling Pag-alala: Caloocan Heritage Tour",
                "icon": "bi-building",
                "description": "A cultural immersion program that reconnects CFAD students with the historical, architectural, and cultural heritage of Caloocan through guided tours, lectures, and discussions with heritage advocates and historians.",
            },
            {
                "title": "Creative Paths: Career Opportunities in CFAD",
                "icon": "bi-briefcase",
                "description": "A career orientation program introducing students to diverse professional opportunities in architecture, fine arts, and design, helping them explore industry pathways and connect with mentors.",
            },
            {
                "title": "CFAD Academic Consultation Day",
                "icon": "bi-calendar-check",
                "description": "A recurring academic support initiative that allows students to review grades, consult with faculty, and receive academic guidance during every Prelim, Midterm, and Finals period.",
            },
            {
                "title": "Colors of Love: CFAD Valentine's Special",
                "icon": "bi-heart",
                "description": "A Valentine's event that combines creative expression with social advocacy through talks on inclusive education and LGBTQIA+ awareness alongside student-led artistic activities celebrating diversity.",
            },
            {
                "title": "CFAD Unified: Connecting Creative Community",
                "icon": "bi-diagram-3",
                "description": "A collaborative program that strengthens communication among CFAD departments and student organizations, ensuring equal representation and a stronger sense of community within the college.",
            },
            {
                "title": "LikahLink: Art in Motion",
                "icon": "bi-palette",
                "description": "A collaborative art event where participants pass around artworks to be continued by other artists, encouraging creativity, spontaneity, and artistic collaboration within the CFAD community.",
            },
            {
                "title": "Studio Sessions: Behind the CFAD Canvas",
                "icon": "bi-mic",
                "description": "A student-led podcast featuring conversations with faculty, students, and alumni about design trends, creative processes, and student experiences, fostering dialogue and inspiration within CFAD.",
            },
            {
                "title": "Habi-Haligi: Weaving Art, Building the Future",
                "icon": "bi-threads",
                "description": "A sustainability-focused workshop that teaches students eco-friendly art techniques such as weaving, transforming creative ideas into functional and environmentally responsible works.",
            },
            {
                "title": "CFAD CoLab: Create, Collaborate, Recharge",
                "icon": "bi-layout-text-window-reverse",
                "description": "A spatial optimization project that converts vacant classrooms into open creative workspaces where students can study, draft, collaborate, and work on projects.",
            },
            {
                "title": "CFAD Inspiration Talks",
                "icon": "bi-lightbulb",
                "description": "A lecture series featuring professional artists, architects, and designers who share their experiences, insights, and career journeys to inspire and guide CFAD students.",
            },
            {
                "title": "Arts & Assets Workshop: Smart Money for Creative Students",
                "icon": "bi-cash-coin",
                "description": "A seminar-workshop that teaches financial literacy for creative students, including budgeting, project costing, pricing artwork, and managing creative projects as sustainable ventures.",
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


@lru_cache(maxsize=1)
def load_candidates() -> list[dict[str, Any]]:
    """Load all candidates from the database, sorted by council and position hierarchy."""
    return database.load_candidates()


def save_candidates(candidates: list[dict[str, Any]]) -> None:
    """Save multiple candidates (replaces all existing data)."""
    return database.save_candidates(candidates)


@lru_cache(maxsize=1)
def load_council_candidates(council_code: str) -> list[dict[str, Any]]:
    """Load candidates filtered by council (cached)."""
    all_candidates = load_candidates()
    return [c for c in all_candidates if c.get("council") == council_code]


def load_messages() -> list[dict[str, Any]]:
    return []


def save_message(message: dict[str, Any]) -> None:
    pass


def _split_credentials_into_sections(credentials: str) -> list[dict[str, Any]]:
    """Parse a raw credentials string into structured sections.
    Each section has a title, an icon, and a list of items.
    This provides a consistent UI for credentials across candidates.

    Known section headers are normalized to icons for display.
    """
    if not credentials:
        return []
    # Map common headers to Bootstrap icons
    header_icons = {
        "ACADEMIC EXCELLENCE": "bi-mortarboard-fill",
        "EXTRA CURRICULARS": "bi-star-fill",
        "INTERNATIONAL LEVEL": "bi-globe",
        "NATIONAL LEVEL": "bi-diagram-3",
        "REGIONAL LEVEL": "bi-file-earmark-text",
        "CITY-WIDE LEVEL": "bi-map",
        "SCHOOL LEVEL": "bi-book",
        "ACADEMICS": "bi-mortarboard-fill",
        "AWARDS": "bi-trophy",
    }

    lines = [ln.strip() for ln in credentials.split("\n") if ln.strip()]
    sections: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None

    for line in lines:
        key = line.upper()
        if key in header_icons:
            # start a new section
            if current:
                sections.append(current)
            current = {
                "title": line,
                "icon": header_icons.get(key, "bi-info-circle"),
                "items": [],
            }
        else:
            if current is None:
                current = {"title": "Overview", "icon": "bi-info-circle", "items": []}
            current["items"].append(line)

    if current:
        sections.append(current)
    return sections


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
            # Structured sections for UI rendering
            "credentials_sections": _split_credentials_into_sections(credentials),
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
        exact_position = None
        if query == "president":
            exact_position = "President"
        elif query == "vice president":
            exact_position = "Vice President"

        if exact_position:
            filtered = [
                item
                for item in filtered
                if item.get("position", "").lower() == exact_position.lower()
            ]
        else:
            filtered = [
                item
                for item in filtered
                if query in item.get("name", "").lower()
                or query in item.get("position", "").lower()
            ]

    COUNCIL_ORDER = {"CSC": 0, "ENSC": 1, "CASSC": 2, "CBASC": 3, "CFADSC": 4}

    def sort_key(c):
        pos_order = get_position_order(c.get("position", ""))
        council_order = COUNCIL_ORDER.get(c.get("council", ""), 99)
        name = c.get("name", "")
        return (pos_order, council_order, name)

    filtered.sort(key=sort_key)

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

    council_candidates = [
        item for item in all_candidates if item["council"] == candidate["council"]
    ]
    council_candidates.sort(key=lambda x: get_position_order(x.get("position", "")))

    current_index = next(
        (i for i, c in enumerate(council_candidates) if c["id"] == candidate_id), -1
    )

    prev_candidate = (
        council_candidates[current_index - 1] if current_index > 0 else None
    )
    next_candidate = (
        council_candidates[current_index + 1]
        if current_index < len(council_candidates) - 1
        else None
    )

    council = COUNCIL_BY_CODE[candidate["council"]]
    return render_template(
        "candidate_profile.html",
        candidate=candidate,
        council=council,
        prev_candidate=prev_candidate,
        next_candidate=next_candidate,
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

    council_candidates.sort(key=lambda x: get_position_order(x.get("position", "")))

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


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        from datetime import datetime
        from database import save_message

        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_message(
            {
                "name": name,
                "email": email,
                "subject": subject,
                "message": message,
                "created_at": created_at,
            }
        )
        flash("Your message has been recorded!", "success")
        return redirect(url_for("contact"))
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
