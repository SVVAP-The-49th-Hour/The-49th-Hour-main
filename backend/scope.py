import os
import json

from dotenv import load_dotenv
from supabase import create_client
from google import genai


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# SUPABASE SETUP
# ============================================================

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


if not SUPABASE_URL or not SUPABASE_KEY:

    print(" Supabase credentials not found in .env")

    exit()


supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# ============================================================
# GEMINI SETUP
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not GEMINI_API_KEY:

    print(" Gemini API key not found in .env")

    exit()


client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# AI FUNCTION
# ============================================================

def ask_ai(prompt):

    response = client.models.generate_content(

        model="gemini-3.6-flash",

        contents=prompt

    )

    return response.text


# ============================================================
# GET PROJECTS FROM SUPABASE
# ============================================================

print("\n Loading projects from Supabase...\n")


try:

    response = (
        supabase
        .table("projects")
        .select("*")
        .execute()
    )

    projects = response.data

except Exception as e:

    print("\n Could not connect to Supabase.")

    print(e)

    exit()


# ============================================================
# CHECK PROJECTS
# ============================================================

if not projects:

    print(" No projects found in Supabase.")

    exit()


print(
    " Loaded",
    len(projects),
    "projects."
)


# ============================================================
# DISPLAY PROJECTS
# ============================================================

print("\n====================================")
print("        AVAILABLE PROJECTS")
print("====================================\n")


for i in range(len(projects)):

    print(
        str(i + 1) + ".",
        projects[i].get("title")
    )


# ============================================================
# SELECT PROJECT
# ============================================================

choice = input(
    "\nEnter the number of the project you want to analyze:\n> "
)


try:

    choice = int(choice)

except ValueError:

    print("\n Please enter a valid number.")

    exit()


if choice < 1 or choice > len(projects):

    print("\n Invalid project number.")

    exit()


selected_project = projects[choice - 1]


# ============================================================
# DISPLAY SELECTED PROJECT
# ============================================================

print("\n====================================")
print("        SELECTED PROJECT")
print("====================================\n")


print(
    "Title:",
    selected_project.get("title")
)


print(
    "Domain:",
    selected_project.get("track_domain")
)


print(
    "Technology:",
    selected_project.get("tech_stack")
)


print(
    "Description:",
    selected_project.get("description")
)


# ============================================================
# PREPARE PROJECT FOR GEMINI
# ============================================================

project_data = json.dumps(
    selected_project,
    indent=2,
    default=str
)


# ============================================================
# GEMINI ANALYSIS PROMPT
# ============================================================

analysis_prompt = f"""
You are an AI innovation strategist and technology analyst.

You are analyzing a project that originally came from a
hackathon.

Your job is to determine whether this project has potential
beyond the hackathon and how it could evolve into a useful
real-world product.

IMPORTANT:

Analyze the project critically.

Do NOT blindly praise it.

Do NOT invent capabilities that the project does not have
without clearly identifying them as proposed future additions.

Base your analysis primarily on the project's actual
description, domain, technology stack, and status.

Here is the project:

{project_data}


Analyze the following areas:

1. FUTURE SCOPE

Explain:

- How the project could evolve
- What features could be added
- What problems it could eventually solve
- What it could become in 1-3 years


2. INDUSTRY APPLICATIONS

Identify industries that could realistically use this project.

For each industry:

- Name the industry
- Explain the application
- Explain why the project is relevant there


3. PROSPECTIVE USERS

Identify:

- Primary users
- Secondary users
- Organizations
- Potential customers


4. COMMERCIAL POTENTIAL

Determine whether this could realistically become:

- A startup
- A SaaS product
- An enterprise product
- A campus product
- An open-source platform
- Or another type of product

Explain your reasoning.


5. POSSIBLE BUSINESS MODELS

Suggest realistic ways this project could generate revenue.

Examples may include:

- Subscription
- Freemium
- Enterprise licensing
- API access
- Commission
- Hardware + software
- Institutional licensing

Only suggest models that make sense for this project.


6. TECHNOLOGY EVOLUTION

Explain which technologies could improve the project.

Potential examples:

- Artificial intelligence
- Machine learning
- Computer vision
- IoT
- Cloud computing
- Mobile applications
- Edge computing
- Data analytics

Do not add technologies simply because they are popular.


7. SCALABILITY

Explain what would be required to move from:

Hackathon prototype
        ↓
Real-world MVP
        ↓
Large-scale deployment


8. REAL-WORLD CHALLENGES

Identify realistic obstacles such as:

- Technical limitations
- Cost
- Infrastructure
- Data availability
- Privacy
- Security
- Regulation
- Reliability
- User adoption
- Maintenance


9. COMPETITIVE ADVANTAGE

Explain:

- What could make this project different
- What existing solutions might already do
- What would need to improve for this project to compete


10. FUTURE VERSIONS

Create three stages.

VERSION 1:
Improved hackathon prototype

VERSION 2:
Real-world MVP

VERSION 3:
Large-scale product


11. PROJECT SCORES

Give scores from 0-100 for:

Innovation
Industry Potential
Scalability
Commercial Potential
Technical Feasibility
Real-World Usefulness


12. FINAL VERDICT

Give a clear conclusion.

Answer:

"Is this project worth developing beyond the hackathon?"

Explain why.

Do not give an artificially high score just because the
project is a hackathon project.


============================================================
RETURN FORMAT
============================================================

PROJECT:
[Project name]


EXECUTIVE SUMMARY:
[Short but meaningful summary]


FUTURE SCOPE:

[Detailed explanation]


INDUSTRY APPLICATIONS:

1. [Industry]
Application:
[Explanation]

2. [Industry]
Application:
[Explanation]

3. [Industry]
Application:
[Explanation]


PROSPECTIVE USERS:

- [User]
- [User]
- [User]


COMMERCIAL POTENTIAL:

[Analysis]


POSSIBLE BUSINESS MODELS:

- [Model]
- [Model]
- [Model]


TECHNOLOGY EVOLUTION:

- [Technology]
  [Why it helps]

- [Technology]
  [Why it helps]


SCALABILITY:

[Analysis]


REAL_WORLD_CHALLENGES:

- [Challenge]
- [Challenge]
- [Challenge]


COMPETITIVE ADVANTAGE:

[Analysis]


VERSION 1:
[Improved hackathon prototype]


VERSION 2:
[Real-world MVP]


VERSION 3:
[Large-scale product]


INNOVATION_SCORE:
__/100


INDUSTRY_POTENTIAL_SCORE:
__/100


SCALABILITY_SCORE:
__/100


COMMERCIAL_POTENTIAL_SCORE:
__/100


TECHNICAL_FEASIBILITY_SCORE:
__/100


REAL_WORLD_USEFULNESS_SCORE:
__/100


OVERALL_POTENTIAL:
__/100


FINAL_VERDICT:

[Clear conclusion]


============================================================
"""


# ============================================================
# SEND TO GEMINI
# ============================================================

print("\n Gemini is analyzing the project...")
print("This may take a little while.\n")


try:

    analysis_result = ask_ai(
        analysis_prompt
    )

except Exception as e:

    print("\n Gemini API error:")

    print(e)

    exit()


# ============================================================
# DISPLAY RESULT
# ============================================================

print("\n====================================")
print("         FUTURE SCOPE ANALYSIS")
print("====================================\n")


print(analysis_result)


print("\n====================================")
print("             COMPLETE")
print("====================================")