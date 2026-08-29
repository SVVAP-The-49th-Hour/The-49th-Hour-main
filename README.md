# SVVAP: The 49th Hour

The 49th Hour is an archive and collaboration platform for hackathon projects. It indexes project tech stacks, tracks why prototypes stall (team split, technical wall, lack of time), and enables new developer teams to fork the repository and continue development.

## Architecture
This platform uses a flat-file database system:
* **Data Layer:** Hosted in the public `Archive_Database` repository as structured JSON files.
* **Frontend UI Layer:** Fetches data directly from the public GitHub repository endpoints using standard client-side API requests.

## Core Features
* **Project Status Tracking:** Categorizes builds into built, stalled, or abandoned states.
* **Roadblock Mapping:** Logs specific reasons for project stalls to help future contributors evaluate the codebase.
* **Handover Protocol:** Provides direct communication paths and open-source licensing visibility for project hand-offs.

