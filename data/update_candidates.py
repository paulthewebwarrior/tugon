import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import database

def update_candidates():
    updates = [
        {
            "id": "azeah-christel-ortiz-2nd-year-representative",
            "name": "Azeah Christel B. Ortiz",
            "position": "2nd Year Representative",
            "facebook": "https://www.facebook.com/azeahchristel.ortiz",
            "bio": "Azeah Christel B. Ortiz brings a strong background in leadership, campus journalism, and the arts. Passionate and proactive, she is committed to being a dependable voice for students and actively addressing their needs within the academic community.",
            "credentials": "SSG Auditor A.Y. 2018-2019\nClass Officer - Mayor A.Y. 2021-2022\nClass Officer - Vice-Mayor A.Y. 2023-2024\nClass Officer - Treasurer A.Y. 2024-2025\nPresident of Visual Arts Club A.Y. 2024-2025\nThe Crusaders’ Chronicles School Publication - Broadcaster A.Y. 2024-2025\nGraduated at Saint Raphael’s Academy of Legazpi, Inc – With Honors\nOutstanding Club Member of Visual Arts A.Y. 2024-2025\nPerformance Awardee",
            "highlights": [
                "1st Place Collage Making Contest 2022",
                "1st Place Slogan Making Contest 2024",
                "1st Place Poster Making Contest 2024",
                "2nd Place Literary Graphics Making Contest 2023",
                "2nd Place Slogan Making Contest 2023",
                "2nd Place Adolescent Health Summit 2024: Mascot Making Contest",
                "4th Place Best Radio Production in Filipino 2024",
                "4th Place Best News Anchor – Radio Broadcasting DSPC 2024",
                "2018 CSPC Participant – English Radio Broadcasting",
                "2023 DSPC Participant – Filipino Radio Broadcasting",
                "2024 DSPC Participant – Filipino Radio Broadcasting",
                "Araw ng Kabataan sa Lalawigan ng Albay Poster Making Contest 2023 (Participant)",
                "33rd Civil Registration Month PSA–Albay Poster Making Contest 2023 (Participant)"
            ],
            "plan_of_action": "SRA Leadership Training 2023\nSeminar Workshop on Campus Journalism 2023\nLearn, Educate, Advocate Gift Giving & Learning for Youth Progress Seminar 2022\nLinggo ng Kabataan: “Integrational Solidarity Creating a World for All Ages” Seminar 2022\nBACS Journalism Summit 2024 Delegate\nSRA Campus Journalism Training: Be a CJ 2024\n7th Adolescent Health Summit Seminar 2024\nBeyond the Surface: Series 1, 2, & 3 Seminar Workshop 2025\nCFAD Tinakda: Leadership Training 2026"
        },
        {
            "id": "jazzie-vargas-3rd-year-representative",
            "name": "Jazzie Vargas",
            "position": "3rd Year Representative",
            "facebook": "https://www.facebook.com/jazzie.vargas.2025",
            "bio": "Jazzie Vargas combines experience in creative media and student governance, currently serving as the 2nd Year Representative of the CFAD Student Council. Through dedicated service, she continues to amplify student voices and deliver clear and genuine representation.",
            "credentials": "With Honors Grade 7\nTop 3 Overall Grade 7\nWith Honors Grade 8\nWith High Honors Grade 9\nWith High Honors Grade 10\nWith Honors Grade 11\nWith Honors Grade 12\n2nd Year Representative – College of Fine Arts, Architecture, and Design Student Council\nP.I.O – Mathematics Club\nWebsite Manager – The Era Official School Publication of New Era High School\nSchool Paper Layout Artist – The Era Official School Publication\nBest Leader – 21st Century Literature from the Philippines and the World\nCreative Media Committee – UAPSA UE Caloocan\nManlilikha Likhang Komite",
            "highlights": [
                "Member – Pagsulat ng Balita ng Panitik Ngayon",
                "Member – Robotics Club",
                "Member – Mathematics Club"
            ]
        },
        {
            "id": "john-carl-serencio-5th-year-representative",
            "name": "John Carl E. Serencio",
            "position": "5th Year Representative",
            "facebook": "https://www.facebook.com/johncarl.serencio.37",
            "bio": "John Carl E. Serencio, President and former 3rd Year Representative of UAPSA - UE Cal, is known for turning commitments into action. With his focus on clear communication and genuine service, he continues to champion student-centered leadership.",
            "credentials": "3rd Year Representative – United Architects of the Philippines Student Auxiliary (2024–2025)\nChapter President – United Architects of the Philippines Student Auxiliary (2025–2026)",
            "highlights": [
                "Exemplary Award (2024)"
            ]
        },
        {
            "id": "damiane-karl-manzo-public-relations-officer",
            "name": "Damiane Karl Manzo",
            "position": "Public Relations Officer",
            "facebook": "https://www.facebook.com/damiane.manzo",
            "bio": "Damiane Karl Manzo, a Visual Communication student and award-winning creative, has showcased his talent in various art competitions. He advocates for truthful information and active communication to strengthen the connection between the council and the student body.",
            "credentials": "Grade 9 – With Honors\nGrade 10 – With Honors\nGrade 11 – With Honors\nGrade 12 – With Honors",
            "highlights": [
                "BED Chorale",
                "CFAD ARTDECO On-the-Spot Drawing Competition – Champion",
                "UECFAD CDiscenyo – 1st Runner Up",
                "DOST-PNRI Poster Making Competition 2024 – 2nd Runner Up",
                "Valenzuela Visual Arts Society x I Heart Art Poster Making Contest 2025 – 3rd Runner Up",
                "Kundiman sa Silangan 2024 & 2025 – Finalist",
                "Asia and the Pacific Virtual Youth Challenge 2024 – Participant",
                "TNK On-the-Spot Painting Competition – First Honorable Mention",
                "Shell National Student Art Competition – Participant",
                "UST On-the-Spot Painting Competition – Participant",
                "Philippine Fine Jewelry Design Competition – Participant",
                "ArtBeat Exhibition – Artist / Participant",
                "GCCSO Poster Making Contest – Winner (High School)",
                "Consistent Poster Making Participant (Elementary)",
                "Two-Time Tawag ng Silangan Champion (Elementary)",
                "Award for Exceptional Performance in Art (Elementary)",
                "BFP Interschool On-the-Spot Poster Making Contest (Elementary)",
                "ARTEAST – Art Talk",
                "MAG CFADPASOK – CFAD General Assembly",
                "ARTDRENALINE – Art Talk",
                "ARTBATO? – Visual Communication Specialized Talk"
            ]
        },
        {
            "id": "reese-beltran-business-manager",
            "name": "Reese Beltran",
            "position": "Business Manager",
            "facebook": "https://www.facebook.com/reese.molina022006",
            "bio": "Reese Beltran has actively served in the Secretariat Committee and currently works as Ways and Means Director of UAPSA - UE Cal. With her background in coordination and resource management, she focuses on building partnerships and supporting student initiatives.",
            "credentials": "Elementary – Graduated With Honors (2018)\nGrade 8 – With Honors\nGrade 9 – With Honors\nGrade 10 – With Honors\nElementary Student Council Peace Officer Candidate (2016)\nCopyreading and Headline Writing Journalist – District Level (2016)\nUE Visual Arts Member (2022–2023)\nUE Sikhay Silangan Member (2023–2024)\nRanked 29th – UE PUNLASIK: Punlaan ng Karunungan sa Pananaliksik sa Silangan (April 2024)\nUAPSA UE-Caloocan Secretariat Committee (2024–2025)\nUAPSA UE-Caloocan Ways and Means Director (2025–2026)\nUAPSA National COMELEC Creatives Head Chair (2025–2026)",
            "highlights": [
                "Mr. & Ms. Red Cross Youth Leadership Training (2014)",
                "UE 5th PUNLASIK Research Conference (2024)",
                "FEU General Education Experience: Art Appreciation (2024)"
            ]
        },
        {
            "id": "geraldine-paula-cruz-auditor",
            "name": "Geraldine Paula Cruz",
            "position": "Auditor",
            "facebook": "https://www.facebook.com/geraldine.paula.cruz",
            "bio": "Geraldine Paula Cruz, currently the First-Year Representative of the Society of Interior Design Students, values transparency, accountability, and organized service. She is committed to ensuring that every process and resource is handled responsibly.",
            "credentials": "Grade 7 – Honor Student\nGrade 8 – Honor Student\nGrade 9 – Honor Student\nGrade 10 – Honor Student\nGrade 11 – Honor Student\nGrade 12 – Honor Student\nGrade 10 Class Secretary\nSenior High School Art Club Member\n1st Year Representative – Society of Interior Design Students\n1st Year Class Representative",
            "highlights": [
                "Beyond the Surface: Series 1, 2, & 3 Seminar Workshop (2025)",
                "CFAD Tinakda: Leadership Training (2026)"
            ]
        },
        {
            "id": "chryzz-angeline-policarpio-treasurer",
            "name": "Chryzz Angeline Policarpio",
            "position": "Treasurer",
            "facebook": "https://www.facebook.com/chryzzangeline.policarpio.3",
            "bio": "Chryzz Angeline Policarpio, the 1st Year Representative of UAPSA - UE Cal and former Treasurer and Auditor, brings strong experience in financial responsibility. She promotes accountable budgeting and transparent management of student resources.",
            "credentials": "Valedictorian (2018–2019)\nGrade 7 – With High Honors\nGrade 8 – With Honors\nGrade 9 – With Honors\nGrade 10 – With Honors\nGrade 11 – With High Honors\nGrade 12 – With High Honors\nSSG Mayor\nMath Club Treasurer (2021)\nClub Auditor (2023–2024)\nClass Auditor (2024–2025)\nAugustinian Youth Organization Lector and Commentator (2024–2025)\nUAPSA UE-Caloocan 1st Year Representative",
            "highlights": [
                "MTAP Division Level Rank 12 (2020)",
                "ASMEPPS Nationals Qualifier (2021)",
                "ASMEPPS Regionals Participant (2023)"
            ]
        },
        {
            "id": "juliana-marie-betervo-secretary",
            "name": "Juliana Marie Betervo",
            "position": "Secretary",
            "facebook": "https://www.facebook.com/juliana.betervo.3",
            "bio": "Juliana Marie Betervo serves as Public Relations Director of UAPSA - UE Cal and remains active in external affairs and publications. Known for her responsiveness and dedication, she continues to be a trusted and accessible voice for students.",
            "credentials": "Divine Grace School – Graduated With High Honors (2022)\nNational University Fairview – Graduated With High Honors (2024)\nThe Graceans: Ang Patnubay – News Writer and Feature Writer (2018–2022)\nThe Graceans: Ang Patnubay – Feature Editor (2021–2022)\nThe Nationalian Erudites – News and Media Writer (2022–2024)\nNUFV SHS Class Monitor (2022–2024)\nNU Bullpup Slashers Secretary (2023–2024)\nNUFV SHS Humaniteach Student Teacher (2024)\nLualhati League of Scholars Member (2024–2025)\nUAPSA UE-Caloocan Publications Committee (2024–2025)\nUE-Caloocan CFADSC Likhang Komite ng Komunikasyon (2024–2025)\nYFA Humane Education Committee (2024–2025)\nUAPSA UE-Caloocan Public Relations Director (2025–2026)\nSilangan Film Circle External Communications Associate (2025–2026)\nUE-Caloocan CFADSC Likhang Komite ng Pampublikasyon (2025–2026)\nClass Representative (2025–2026)",
            "highlights": [
                "2018 DSSPC Participant – Filipino News Writing",
                "2022 DSSPC Participant – Feature Writing Training Workshop",
                "UAPSA WAD Arkitalks Webinar – Masters of Ceremony (2025)",
                "IN-BETWEEN Spaces: An Architectural Design 8 Lecture Series – Masters of Ceremony (2025)",
                "Edusogno ESL Tutor (2025)",
                "GreenSeashells Freelance Wellness Blog Writer (2025–Present)"
            ]
        },
        {
            "id": "amyline-lopez-vice-president",
            "name": "Ma. Amyline C. Lopez",
            "position": "Vice President",
            "facebook": "https://www.facebook.com/amyline.lopez",
            "bio": "Ma. Amyline C. Lopez, a 3rd Year Architecture student, previously served as Treasurer of the CFAD Student Council and now holds the same position in the Central Student Council, alongside her experience as 2nd Year Representative of UAPSA - UE Cal. Her leadership centers on transparency, accountability, and the pursuit of accessible education.",
            "credentials": "Elementary – Academic Excellence Award\nHigh School – Academic Excellence Award\nSenior High School – Graduated With High Honors\nGrade 5 Supreme Pupil Government Peace Officer\nGrade 7 Math Club Secretary\nGrade 9 Representative – Red Cross Youth Council\n2nd Year Representative – UAPSA UE Caloocan (2024–2025)\nTreasurer – College of Fine Arts, Architecture, and Design Student Council (2024–2025)",
            "highlights": [
                "Champion – Reader’s Theater",
                "1st Place – District Palaro Table Tennis",
                "Choir Member – San Bartolome Parish (2014–2015)",
                "Lector and Commentator – San Bartolome Parish"
            ]
        },
        {
            "id": "shekinah-joy-roxas-president",
            "name": "Shekinah Joy Roxas",
            "position": "President",
            "facebook": "https://www.facebook.com/kumikinah/",
            "bio": "Shekinah Joy Roxas is known for principled leadership and involvement in various student organizations, having served as both Secretary and President. Guided by accountability, advocacy, and service, he champions artistic expression as a tool for meaningful change and inclusive representation.",
            "credentials": "Exemplary Performance in Academic Excellence (2024–2025)\nChief Executive Officer – Youth for Animals PAWS UE Caloocan (2025–2026)\nExecutive Secretary – Buklod Sining Organization (2025–2026)\n2nd Year Representative – Buklod Sining Organization (2024–2025)\nMultimedia Chairperson – Youth for Animals PAWS UE Caloocan (2024–2025)\nPublic Relations Associate Staff – Central Student Council (2024–2025)\nTechnical Committee – Likhang Komite (2024–2025)\nCreatives Committee – Youth for Animals UE Caloocan (2023–2024)",
            "highlights": [
                "Exemplary Performance in Visual Arts and Design (2025)",
                "Templo ng Katabaan “Sining ang Bagong Pagasa ng Kabataan” On-the-Spot Drawing and Painting Contest – First Place (2024)",
                "Naratibo ng Silangan On-the-Spot Drawing Competition – Grand Prize Winner (2023)"
            ]
        }
    ]
    for cand in updates:
        # Ensure brief_introduction is set for frontend display
        if "bio" in cand:
            cand["brief_introduction"] = cand["bio"]
        # Try to find candidate by id first
        existing = database.get_candidate(cand["id"])
        # If not found by id, try by name (to ensure correct mapping)
        if not existing:
            # Try to find by name (case-insensitive)
            all_candidates = database.get_all_candidates() if hasattr(database, 'get_all_candidates') else []
            for c in all_candidates:
                if c.get("name", "").strip().lower() == cand["name"].strip().lower():
                    existing = c
                    break
        if existing:
            existing.update(cand)
            database.save_candidate(existing)
        else:
            database.save_candidate(cand)
    print("Candidate updates complete.")

if __name__ == "__main__":
    update_candidates()
