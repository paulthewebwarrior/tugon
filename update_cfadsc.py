import sqlite3

conn = sqlite3.connect("data/tugon.db")
cursor = conn.cursor()

candidates = {
    "cfadsc-azeah-christel-ortiz": {
        "tagline": "Azeah Christel B. Ortiz brings a strong background in leadership, campus journalism, and the arts. Passionate and proactive, she is committed to being a dependable voice for students and actively addressing their needs within the academic community.",
        "credentials": """LEADERSHIP & EDUCATION
SSG Auditor (A.Y. 2018-2019)
Class Officer - Mayor (A.Y. 2021-2022)
Class Officer - Vice Mayor (A.Y. 2023-2024)
Class Officer - Treasurer (A.Y. 2024-2025)
President, Visual Arts Club (A.Y. 2024-2025)
Broadcaster, The Crusaders' Chronicles School Publication (A.Y. 2024-2025)
Graduated with Honors - Saint Raphael's Academy of Legazpi, Inc.
Outstanding Club Member - Visual Arts (A.Y. 2024-2025)
Performance Awardee
EXTRACURRICULAR ACTIVITIES
1st Place - Collage Making Contest (2022)
1st Place - Slogan Making Contest (2024)
1st Place - Poster Making Contest (2024)
2nd Place - Literary Graphics Making Contest (2023)
2nd Place - Slogan Making Contest (2023)
2nd Place - Adolescent Health Summit Mascot Making Contest (2024)
4th Place - Best Radio Production in Filipino (2024)
4th Place - Best News Anchor, Radio Broadcasting DSPC (2024)
Participant - English Radio Broadcasting CSPC (2018)
Participant - Filipino Radio Broadcasting DSPC (2023)
Participant - Filipino Radio Broadcasting DSPC (2024)
Participant - Araw ng Kabataan sa Lalawigan ng Albay Poster Making Contest (2023)
Participant - 33rd Civil Registration Month PSA-Albay Poster Making Contest (2023)
TRAININGS & SEMINARS
SRA Leadership Training (2023)
Seminar Workshop on Campus Journalism (2023)
Learn, Educate, Advocate: Gift Giving & Learning for Youth Progress Seminar (2022)
Linggo ng Kabataan: "Integrational Solidarity Creating a World for All Ages" Seminar (2022)
BACS Journalism Summit Delegate (2024)
SRA Campus Journalism Training: Be a CJ (2024)
7th Adolescent Health Summit Seminar (2024)
Beyond the Surface: Series 1, 2, & 3 Seminar Workshop (2025)
CFAD Tinakda: Leadership Training (2026)""",
        "facebook": "https://www.facebook.com/azeahchristel.ortiz",
    },
    "cfadsc-jazzie-vargas": {
        "tagline": "Jazzie Vargas combines experience in creative media and student governance, currently serving as the 2nd Year Representative of the CFAD Student Council. Through dedicated service, she continues to amplify student voices and deliver clear and genuine representation.",
        "credentials": """ACADEMICS
With Honors - Grade 7
Top 3 Overall - Grade 7
With Honors - Grade 8
With High Honors - Grade 9
With High Honors - Grade 10
With Honors - Grade 11
With Honors - Grade 12
LEADERSHIP
2nd Year Representative - College of Fine Arts, Architecture, and Design Student Council
P.I.O - Mathematics Club
Website Manager - The Era, Official School Publication of New Era High School
School Paper Layout Artist - The Era, Official School Publication of New Era High School
Best Leader - 21st Century Literature from the Philippines and the World
Creative Media Committee - UAPSA UE Caloocan
Manlilikha - Likhang Komite
EXTRACURRICULARS
Member - Pagsulat ng Balita, Panitik Ngayon
Member - Robotics Club
Member - Mathematics Club""",
        "facebook": "https://www.facebook.com/jazzie.vargas.2025",
    },
    "cfadsc-john-carl-serencio": {
        "tagline": "John Carl E. Serencio, President and former 3rd Year Representative of UAPSA - UE Cal, is known for turning commitments into action. With his focus on clear communication and genuine service, he continues to champion student-centered leadership.",
        "credentials": """AWARDS
Exemplary Award (2024)
LEADERSHIP
3rd Year Representative - United Architects of the Philippines Student Auxiliary (2024-2025)
Chapter President - United Architects of the Philippines Student Auxiliary (2025-2026)""",
        "facebook": "https://www.facebook.com/johncarl.serencio.37",
    },
    "cfadsc-damiane-karl-manzo": {
        "tagline": "Damiane Karl Manzo, a Visual Communication student and award-winning creative, has showcased his talent in various art competitions. He advocates for truthful information and active communication to strengthen the connection between the council and the student body.",
        "credentials": """ACADEMICS
Grade 9 - With Honors
Grade 10 - With Honors
Grade 11 - With Honors
Grade 12 - With Honors
EXTRACURRICULARS & AWARDS
BED Chorale
CFAD ARTDECO On-the-Spot Drawing Competition - Champion
UECFAD CDiscenyo - 1st Runner-Up
DOST-PNRI Poster Making Competition - 2nd Runner-Up (2024)
Valenzuela Visual Arts Society x I Heart Art Poster Making Contest - 3rd Runner-Up (2025)
Kundiman sa Silangan - Finalist (2024 & 2025)
Asia and the Pacific Virtual Youth Challenge - Participant (2024)
TNK On-the-Spot Painting Competition - First Honorable Mention
Shell National Student Art Competition - Participant
UST On-the-Spot Painting Competition - Participant
Philippine Fine Jewelry Design Competition - Participant
ArtBeat Exhibition - Artist / Participant
GCCSO Poster Making Contest - Winner (High School)
Consistent Poster Making Participant (Elementary)
Two-Time Tawag ng Silangan Champion (Elementary)
Award for Exceptional Performance in Art (Elementary)
BFP Interschool On-the-Spot Poster Making Contest (Elementary)
SEMINARS & WORKSHOPS
ARTEAST - Art Talk
MAG CFADPASOK - CFAD General Assembly
ARTDRENALINE - Art Talk
ARTBATO? - Visual Communication Specialized Talk""",
        "facebook": "https://www.facebook.com/damiane.manzo",
    },
    "cfadsc-reese-beltran": {
        "tagline": "Reese Beltran has actively served in the Secretariat Committee and currently works as Ways and Means Director of UAPSA - UE Cal. With her background in coordination and resource management, she focuses on building partnerships and supporting student initiatives.",
        "credentials": """ACADEMICS
Elementary - Graduated with Honors (2018)
Grade 8 - With Honors
Grade 9 - With Honors
Grade 10 - With Honors
LEADERSHIP & EXTRACURRICULARS
Elementary Student Council Peace Officer Candidate (2016)
Copyreading and Headline Writing Journalist - District Level (2016)
UE Visual Arts Member (2022-2023)
UE Sikhay Silangan Member (2023-2024)
Ranked 29th - UE PUNLASIK Research Conference (April 2024)
UAPSA UE-Caloocan Secretariat Committee (2024-2025)
UAPSA UE-Caloocan Ways and Means Director (2025-2026)
UAPSA National COMELEC Creatives Head Chair (2025-2026)
SEMINARS & WORKSHOPS
Mr. & Ms. Red Cross Youth Leadership Training (2014)
UE 5th PUNLASIK Research Conference (2024)
FEU General Education Experience: Art Appreciation (2024)""",
        "facebook": "https://www.facebook.com/reese.molina022006",
    },
    "cfadsc-geraldine-paula-cruz": {
        "tagline": "Geraldine Paula Cruz, currently the First-Year Representative of the Society of Interior Design Students, values transparency, accountability, and organized service. She is committed to ensuring that every process and resource is handled responsibly.",
        "credentials": """ACADEMICS
Honor Student - Grade 7
Honor Student - Grade 8
Honor Student - Grade 9
Honor Student - Grade 10
Honor Student - Grade 11
Honor Student - Grade 12
LEADERSHIP & EXTRACURRICULARS
Grade 10 Class Secretary
Senior High School Art Club Member
1st Year Representative - Society of Interior Design Students
1st Year Class Representative
SEMINARS
Beyond the Surface: Series 1, 2, & 3 Seminar Workshop (2025)
CFAD Tinakda: Leadership Training (2026)""",
        "facebook": "https://www.facebook.com/geraldine.paula.cruz",
    },
    "cfadsc-chryzz-angeline-policarpio": {
        "tagline": "Chryzz Angeline Policarpio, the 1st Year Representative of UAPSA - UE Cal and former Treasurer and Auditor, brings strong experience in financial responsibility. She promotes accountable budgeting and transparent management of student resources.",
        "credentials": """ACADEMICS
Valedictorian (2018-2019)
Grade 7 - With High Honors
Grade 8 - With Honors
Grade 9 - With Honors
Grade 10 - With Honors
Grade 11 - With High Honors
Grade 12 - With High Honors
LEADERSHIP
SSG Mayor
Math Club Treasurer (2021)
Club Auditor (2023-2024)
Class Auditor (2024-2025)
Augustinian Youth Organization Lector and Commentator (2024-2025)
UAPSA UE-Caloocan 1st Year Representative
AWARDS
MTAP Division Level Rank 12 (2020)
ASMEPPS Nationals Qualifier (2021)
ASMEPPS Regionals Participant (2023)""",
        "facebook": "https://www.facebook.com/chryzzangeline.policarpio.3",
    },
    "cfadsc-juliana-marie-betervo": {
        "tagline": "Juliana Marie Betervo serves as Public Relations Director of UAPSA - UE Cal and remains active in external affairs and publications. Known for her responsiveness and dedication, she continues to be a trusted and accessible voice for students.",
        "credentials": """ACADEMICS
Divine Grace School - Graduated with High Honors (2022)
National University Fairview - Graduated with High Honors (2024)
LEADERSHIP & ORGANIZATIONS
News Writer & Feature Writer - The Graceans: Ang Patnubay (2018-2022)
Feature Editor - The Graceans: Ang Patnubay (2021-2022)
News & Media Writer - The Nationalian Erudites (2022-2024)
NUFV SHS Class Monitor (2022-2024)
NU Bullpup Slashers Secretary (2023-2024)
NUFV SHS Humaniteach Student Teacher (2024)
Lualhati League of Scholars Member (2024-2025)
UAPSA UE-Caloocan Publications Committee (2024-2025)
UE-Caloocan CFADSC Likhang Komite ng Komunikasyon (2024-2025)
YFA Humane Education Committee (2024-2025)
UAPSA UE-Caloocan Public Relations Director (2025-2026)
Silangan Film Circle External Communications Associate (2025-2026)
UE-Caloocan CFADSC Likhang Komite ng Pampublikasyon (2025-2026)
Class Representative (2025-2026)
SEMINARS & COMPETITIONS
DSSPC Participant - Filipino News Writing (2018)
DSSPC Participant - Feature Writing Training Workshop (2022)
UAPSA WAD Arkitalks Webinar - Masters of Ceremony (2025)
IN-BETWEEN Spaces: Architectural Design 8 Lecture Series - Masters of Ceremony (2025)
WORK
Edusogno ESL Tutor (2025)
GreenSeashells Freelance Wellness Blog Writer (2025-Present)""",
        "facebook": "https://www.facebook.com/juliana.betervo.3",
    },
    "cfadsc-ma-amyline-lopez": {
        "tagline": "Ma. Amyline C. Lopez, a 3rd Year Architecture student, previously served as Treasurer of the CFAD Student Council and now holds the same position in the Central Student Council. Her leadership centers on transparency, accountability, and the pursuit of accessible education.",
        "credentials": """ACADEMIC EXCELLENCE
Elementary - Academic Excellence Award
High School - Academic Excellence Award
Senior High School - Graduated with High Honors
LEADERSHIP
Grade 5 Supreme Pupil Government Peace Officer
Grade 7 Math Club Secretary
Grade 9 Representative - Red Cross Youth Council
2nd Year Representative - UAPSA UE Caloocan (2024-2025)
Treasurer - College of Fine Arts, Architecture, and Design Student Council (2024-2025)
EXTRACURRICULARS
Champion - Reader's Theater
1st Place - District Palaro Table Tennis
Choir - San Bartolome Parish (2014-2015)
Lector and Commentator - San Bartolome Parish""",
        "facebook": "https://www.facebook.com/amyline.lopez",
    },
    "cfadsc-shekinah-joy-roxas": {
        "tagline": "Shekinah Joy Roxas is known for principled leadership and involvement in various student organizations. Guided by accountability, advocacy, and service, he champions artistic expression as a tool for meaningful change and inclusive representation.",
        "credentials": """ACADEMICS
Exemplary Performance in Academic Excellence (2024-2025)
LEADERSHIP
2025-2026
Chief Executive Officer - Youth for Animals PAWS UE Caloocan
Executive Secretary - Buklod Sining Organization
2024-2025
2nd Year Representative - Buklod Sining Organization
Multimedia Chairperson - Youth for Animals PAWS UE-Cal
Public Relations Associate Staff - Central Student Council
Technical Committee - Likhang Komite
2023-2024
Creatives Committee - Youth for Animals UE-Cal
EXTRACURRICULARS & AWARDS
2025
Exemplary Performance in Visual Arts and Design
2024
Templo ng Katabaan "Sining ang Bagong Pagasa ng Kabataan" On-the-Spot Drawing and Painting Contest - First Place
2023
"Naratibo ng Silangan" On-the-Spot Drawing Competition - Grand Prize Winner""",
        "facebook": "https://www.facebook.com/kumikinah/",
    },
}

for cid, data in candidates.items():
    cursor.execute(
        "UPDATE candidates SET tagline = ?, credentials = ?, facebook = ? WHERE id = ?",
        (data["tagline"], data["credentials"], data.get("facebook", ""), cid),
    )
    print(f"Updated: {cid}")

conn.commit()
conn.close()
print("Done!")
