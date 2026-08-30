import os
import json
import re

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


if len(projects) < 2:

    print(" At least two projects are required.")

    exit()


print(
    " Loaded",
    len(projects),
    "projects."
)


# ============================================================
# NUMBER THE PROJECTS
# ============================================================

numbered_projects = []


for i in range(len(projects)):

    project = projects[i]

    numbered_projects.append({

        "project_number": i + 1,

        "title": project.get("title"),

        "track_domain": project.get("track_domain"),

        "tech_stack": project.get("tech_stack"),

        "description": project.get("description"),

        "status": project.get("status"),

        "status_details": project.get("status_details")

    })


# ============================================================
# CONVERT PROJECTS TO JSON
# ============================================================

project_list = json.dumps(

    numbered_projects,

    indent=2,

    default=str

)


# ============================================================
# GET TWO DIFFERENT KEYWORDS
# ============================================================

print("\n====================================")
print("       PROJECT FUSION ENGINE")
print("====================================\n")


keyword1 = input(
    "Enter the FIRST idea / keyword:\n> "
)


keyword2 = input(
    "\nEnter the SECOND idea / keyword:\n> "
)


# ============================================================
# FUNCTION TO FIND CLOSEST PROJECT
# ============================================================

def find_closest_project(keyword):

    prompt = f"""
You are an AI system that searches a database of hackathon
projects.

The user has provided this search keyword:

"{keyword}"

Your job is ONLY to find the SINGLE project that is most
relevant to this keyword.

DO NOT merge anything.

DO NOT create a new idea.

DO NOT modify the project.

Analyze the projects based on:

- Problem domain
- Purpose
- Target users
- Features
- Technologies
- Overall conceptual relevance

Here is the database:

{project_list}

Every project has a PROJECT NUMBER.

You MUST return the PROJECT NUMBER of the best match.

Return ONLY this format:

PROJECT_NUMBER:
[number]

PROJECT_TITLE:
[title]

MATCH_SCORE:
[number from 1-100]

REASON:
[short explanation]
"""

    return ask_ai(prompt)


# ============================================================
# FIND PROJECT FOR KEYWORD 1
# ============================================================

print("\n Searching for the closest project to:")

print(keyword1)


result1 = find_closest_project(keyword1)


print("\n====================================")
print("        MATCH FOR KEYWORD 1")
print("====================================\n")


print(result1)


# ============================================================
# FIND PROJECT FOR KEYWORD 2
# ============================================================

print("\n Searching for the closest project to:")

print(keyword2)


result2 = find_closest_project(keyword2)


print("\n====================================")
print("        MATCH FOR KEYWORD 2")
print("====================================\n")


print(result2)


# ============================================================
# EXTRACT PROJECT NUMBERS
# ============================================================

def extract_project_number(result):

    match = re.search(

        r"PROJECT_NUMBER:\s*(\d+)",

        result,

        re.IGNORECASE

    )

    if match:

        return int(
            match.group(1)
        )

    return None


project_number1 = extract_project_number(
    result1
)


project_number2 = extract_project_number(
    result2
)


# ============================================================
# CHECK RESULTS
# ============================================================

if project_number1 is None:

    print(
        "\n Could not determine the project for keyword 1."
    )

    exit()


if project_number2 is None:

    print(
        "\n Could not determine the project for keyword 2."
    )

    exit()


# ============================================================
# CHECK PROJECT NUMBERS
# ============================================================

if project_number1 < 1 or project_number1 > len(projects):

    print(
        "\n AI returned an invalid project number for keyword 1."
    )

    exit()


if project_number2 < 1 or project_number2 > len(projects):

    print(
        "\n AI returned an invalid project number for keyword 2."
    )

    exit()


# ============================================================
# GET ACTUAL PROJECTS
# ============================================================

project1 = projects[
    project_number1 - 1
]


project2 = projects[
    project_number2 - 1
]


# ============================================================
# MAKE SURE THEY ARE DIFFERENT
# ============================================================

if project_number1 == project_number2:

    print("\n Both keywords selected the same project.")

    print(
        "\nProject:",
        project1.get("title")
    )

    print(
        "\nThe two keywords need to correspond "
        "to two different projects."
    )

    exit()


# ============================================================
# DISPLAY SELECTED PROJECTS
# ============================================================

print("\n====================================")
print("        SELECTED PROJECTS")
print("====================================\n")


print(
    "🔹 Keyword 1:",
    keyword1
)


print(
    "   Project:",
    project1.get("title")
)


print()


print(
    "🔹 Keyword 2:",
    keyword2
)


print(
    "   Project:",
    project2.get("title")
)


# ============================================================
# CHECK MERGE FEASIBILITY
# ============================================================

print(
    "\nEvaluating whether the two projects can be merged...\n"
)


feasibility_prompt = f"""
You are an AI system that evaluates whether TWO DIFFERENT
hackathon projects can be meaningfully combined.

PROJECT 1:

{json.dumps(project1, indent=2, default=str)}


PROJECT 2:

{json.dumps(project2, indent=2, default=str)}


Evaluate whether these projects can be combined into ONE
new project.

Consider:

1. Problem compatibility
2. Target-user compatibility
3. Feature compatibility
4. Technology compatibility
5. Whether one project's capabilities complement the other
6. Technical feasibility
7. Real-world usefulness
8. Whether combining them creates something genuinely new

IMPORTANT:

Do NOT merge them yet.

First determine whether the combination makes sense.

Give ONE overall feasibility score from 0 to 100.

Return ONLY:

FEASIBILITY_SCORE:
[number]/100

REASON:
[Detailed explanation]

MERGE_POTENTIAL:
[Explain how the projects could potentially complement
each other, or why they should remain separate]
"""


feasibility_result = ask_ai(
    feasibility_prompt
)


# ============================================================
# DISPLAY FEASIBILITY
# ============================================================

print("\n====================================")
print("        MERGE FEASIBILITY")
print("====================================\n")


print(feasibility_result)


# ============================================================
# EXTRACT SCORE
# ============================================================

score_match = re.search(

    r"FEASIBILITY_SCORE:\s*(\d+)",

    feasibility_result,

    re.IGNORECASE

)


if score_match:

    feasibility_score = int(
        score_match.group(1)
    )

else:

    feasibility_score = 0


print(
    "\nFeasibility:",
    str(feasibility_score) + "/100"
)


# ============================================================
# MERGE THRESHOLD
# ============================================================

MERGE_THRESHOLD = 70


if feasibility_score < MERGE_THRESHOLD:

    print("\n====================================")
    print("       MERGE NOT RECOMMENDED")
    print("====================================\n")


    print(
        "The projects are not compatible enough."
    )


    print(
        "Required:",
        str(MERGE_THRESHOLD) + "/100"
    )


    print(
        "Actual:",
        str(feasibility_score) + "/100"
    )


    exit()


# ============================================================
# MERGE THE TWO PROJECTS
# ============================================================

print("\n====================================")
print("        MERGING PROJECTS")
print("====================================\n")


merge_prompt = f"""
You are an AI innovation engine.

Two different hackathon projects have been evaluated and
their compatibility score is high enough to justify combining
them.

PROJECT 1:

{json.dumps(project1, indent=2, default=str)}


PROJECT 2:

{json.dumps(project2, indent=2, default=str)}


FEASIBILITY SCORE:

{feasibility_score}/100


Create ONE genuinely new project by combining the strongest
and most useful aspects of both projects.

IMPORTANT:

Do NOT simply combine their names.

Do NOT simply put all their features together.

Find a meaningful connection between their capabilities.

The new project must:

- Use meaningful aspects of BOTH projects
- Solve a real problem
- Provide functionality that neither project provides alone
- Be technically feasible
- Be realistic for a college hackathon
- Have potential for real-world implementation

Return:

NEW PROJECT NAME:
[Name]

CORE PROBLEM:
[Problem]

FUSED IDEA:
[Detailed explanation]

PROJECT 1 CONTRIBUTION:
[What Project 1 contributes]

PROJECT 2 CONTRIBUTION:
[What Project 2 contributes]

THE BRIDGE:
[Why these two projects work together]

WHAT MAKES IT UNIQUE:
[Novel aspect]

HOW IT WORKS:
1.
2.
3.
4.

REQUIRED TECHNOLOGIES:
[List technologies]

REAL_WORLD_APPLICATION:
[How it could be used]

FINAL_FEASIBILITY:
__/100

NOVELTY_SCORE:
__/100

USEFULNESS_SCORE:
__/100

FINAL_VERDICT:
[Why this fusion is or is not worth building]
"""


merge_result = ask_ai(
    merge_prompt
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n====================================")
print("           FUSED PROJECT")
print("====================================\n")


print(merge_result)


print("\n====================================")
print("             COMPLETE")
print("====================================")