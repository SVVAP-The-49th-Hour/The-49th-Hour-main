**Core Architecture and Stack**

The platform operates on a modern, asynchronous Python backend tailored for AI integration and real-time collaboration.

* **Framework:** FastAPI handling asynchronous REST endpoints, middleware, and dependency injection.
* **Database:** MongoDB (via Motor AsyncIO) serving as the primary document store for users, projects, conversations, and messages.
* **AI Integration:** `emergentintegrations.llm.chat` powering custom GPT-5.4 prompts for project analysis.
* **Object Storage:** Proxy-based storage (`integrations.emergentagent.com`) for handling ZIP file uploads.
* **External Sync:** Supabase integration for mirroring and retrieving external project databases.
* **Security:** JWT-based authentication (access/refresh tokens) via secure HTTP-only cookies and bcrypt password hashing.

**Authentication and Identity Management**

The platform features a robust, secure user management system designed to track individual makers and their portfolios.

* **Registration and Login:** Users register with a unique username, email, and password. Passwords are salted and hashed via bcrypt. The login system supports authenticating via either email or username.
* **Session Handling:** JWTs securely manage sessions. An access token (valid for 30 minutes) and a refresh token (valid for 7 days) are issued as HTTP-only, secure, `SameSite=none` cookies, ensuring safety against XSS attacks while allowing cross-origin resource sharing (CORS).
* **User Profiles:** Profiles publicly display a user's join date, username, their owned projects, and their saved/bookmarked projects.

**The Project Archive Engine**

The core functionality revolves around a dynamic repository of hackathon projects—categorized primarily as Stalled, Built, or Abandoned.

* **Project Ingestion:** Users can submit projects by defining the title, hackathon name, tech stack (tags), current status, stall reasons, GitHub links, and willingness to collaborate.
* **Supabase Synchronization:** The system can automatically sync records from an external Supabase table. It normalizes project statuses (e.g., converting "dead" to "Abandoned") and avoids duplicating entries, creating a unified timeline of projects.
* **Claiming and Saving:** Users can bookmark projects of interest to their private "Saved" list. Furthermore, orphaned projects ingested from external archives can be officially claimed by users, transferring ownership to their account.
* **Instant Feasibility Checks:** Upon creating a new project, the system instantly cross-references the database to find the closest existing project and calculates a preliminary feasibility score for combining them.

**AI Analysis and The Fusion Engine**

The platform's standout feature is its AI-driven capability to evaluate and merge disparate concepts.

* **Project Scope Analysis:** Users can trigger an AI evaluation of any project. The system prompts a GPT-5.4 model acting as an innovation analyst to critique the project. It generates a structured report identifying industry applications, commercial potential, real-world challenges, and scopes out three evolutionary versions (Hackathon Prototype, MVP, Large-scale product) alongside scored metrics.
* **The Fusion Engine:** Users can input two keywords to search the archive. The AI strictly identifies the best matching project for each keyword. If two distinct projects are found, it generates a Feasibility Score.
* **AI Merging:** If the feasibility score exceeds the threshold (70/100), the AI generates a Fused Idea—a brand new product architecture that synthesizes the technical strengths and features of both original projects into a novel application.

**Collaboration and Messaging**

To bring fused projects to life, the platform includes a native, asynchronous chat system.

* **Direct Messaging (DMs):** Users can initiate direct conversations to discuss project details.
* **Channels:** Support for multi-user channels (e.g., specific project rooms) allowing groups of makers to coordinate.
* **Threaded Replies:** Messages support a `reply_to` reference, capturing a snapshot of the original message to maintain context in busy channels.
* **AI Fusion Connect:** When users decide to act on an AI-fused project, the platform can automatically generate a DM between the respective project owners, pre-populating a contextual introductory message to kickstart collaboration.

**File and Asset Storage**

* **Codebase Archiving:** Users can upload `.zip` archives of their hackathon code (up to 50 MB).
* **Proxy Storage Integration:** Files are piped securely to an external object store via an initialized `X-Storage-Key`, ensuring the platform itself does not bottleneck on heavy I/O operations. Download routes safely stream these assets back to users.
