# NEXUS

**A personal home automation and AI system designed to connect devices, services, and an intelligent agent into one unified system.**

NEXUS is being developed as a modular home automation platform with a local server handling command processing and a separate terminal providing the user interface. The long-term goal is to build a system that can understand natural-language requests, interact with connected home devices and provide a convenient voice-controlled interface.

The project is being developed incrementally, with an emphasis on modular architecture, practical experimentation, and understanding the technologies involved.

## Project Architecture

NEXUS is the overall system. Its components have distinct responsibilities:

| Component               | Responsibility                                                          |
| ----------------------- | ----------------------------------------------------------------------- |
| **NEXUS**               | The overall home automation and AI project.                             |
| **Nico**                | The assistant persona through which users interact with the system.     |
| **Nico Terminal**       | The user interface, initially running on a Vivo Y95 smartphone.         |
| **NEXUS Server**        | The backend responsible for receiving requests and processing commands. |
| **Command Processor**   | Interprets supported commands and returns structured results.           |
| **Device Integrations** | Planned modules for communicating with compatible home devices.         |

### Current Architecture

```text
                 NICO TERMINAL
                   Vivo Y95
                       |
                       | HTTP
                       v
              NEXUS SERVER
                Windows PC
                       |
                 +-----+-----+
                 |           |
                 v           v
              FastAPI     Core Logic
                 |           |
                 |           v
                 |    Command Processor
                 |           |
                 +-----+-----+
                       |
                       v
                Structured Result
                       |
                       v
                Nico Terminal
```

During development, the NEXUS server runs on a Windows laptop connected to the home network. The Vivo Y95 acts as a separate client rather than hosting the backend itself.

## Technology Stack

| Technology     | Purpose                                          |
| -------------- | ------------------------------------------------ |
| Python         | Backend development and command processing       |
| FastAPI        | HTTP API and request handling                    |
| Uvicorn        | ASGI server used to run the API                  |
| Pydantic       | Request data validation                          |
| HTML           | Nico Terminal's basic web interface              |
| CSS            | Basic client-side presentation                   |
| JavaScript     | Sends commands to the API and displays responses |
| Git and GitHub | Version control and project hosting              |

## Implemented Features

### 1. Network Communication

* Established network communication between the development laptop and the Vivo Y95.
* Verified connectivity over the home Wi-Fi network.
* Confirmed that the Vivo Y95 can access the laptop-hosted web client and API.

### 2. NEXUS API

The FastAPI backend currently provides the following endpoints:

| Endpoint   | Method | Purpose                                                                   |
| ---------- | ------ | ------------------------------------------------------------------------- |
| `/`        | GET    | Returns basic system information.                                         |
| `/status`  | GET    | Returns the current basic system status.                                  |
| `/command` | POST   | Processes a submitted command and returns a structured result.            |
| `/docs`    | GET    | Provides FastAPI's automatically generated interactive API documentation. |

The API is hosted on the development laptop during local development.

### 3. Command System v2

The command processor supports predefined commands, input normalization, aliases, and structured responses.

Implemented capabilities include:

* **Input normalization:** Removes unnecessary surrounding and repeated whitespace and standardizes letter casing.
* **Command registry:** Stores supported commands and their associated metadata.
* **Alias resolution:** Maps supported alternative phrases to canonical commands.
* **Intent identification:** Associates recognized commands with identifiers describing their purpose.
* **Structured results:** Returns fields such as `recognized`, `category`, `intent`, `device`, `action`, `execution_status`, and `response`.
* **Dynamic time response:** Retrieves the development server's local time.
* **Unknown-command handling:** Returns a controlled response when a command is not recognized.

#### Example Supported Commands

| Command           | Current Behaviour                                                            |
| ----------------- | ---------------------------------------------------------------------------- |
| `hello`           | Returns a greeting.                                                          |
| `status`          | Returns a predefined NEXUS status response.                                  |
| `time`            | Returns the current time on the server.                                      |
| `help`            | Lists supported commands.                                                    |
| `turn on the tv`  | Recognizes the requested action but does not control the TV.                 |
| `turn off the tv` | Recognizes the requested action but does not control the TV.                 |
| `lights status`   | Recognizes a light-status request but cannot retrieve actual device status.  |
| `camera status`   | Recognizes a camera-status request but cannot retrieve actual device status. |

Alternative phrases are supported for selected commands through an alias mapping.

**Current limitation:** Command recognition is rule-based. The system does not yet provide general natural-language understanding, and recognizing a device command does not mean that the requested action has been executed.

### 4. Nico Terminal

A basic HTML client has been created for the Vivo Y95.

Current capabilities:

* Accepts text commands.
* Sends HTTP requests to the NEXUS API.
* Displays the responses returned by the server.
* Provides the initial interface for future voice and home-control features.

The client and API are hosted separately during development.

### 5. Development Environment

* Python virtual environment configured.
* Required Python packages recorded in `requirements.txt`.
* Git repository connected to GitHub.
* `.gitignore` configured to exclude virtual environments, common generated files, and environment-variable files.

## Repository Structure

```text
nexus/
├── client/
│   └── index.html
│
├── server/
│   ├── api/
│   ├── config/
│   ├── core/
│   │   └── command_processor.py
│   └── main.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

Some directories are reserved for future modules and may currently be empty.

## Setup and Local Development

### Prerequisites

* Python installed on the development machine.
* Git installed and configured.
* A browser for testing the API and web client.

### 1. Clone the Repository

```bash
git clone https://github.com/AdiDev1512006/nexus.git
cd nexus
```

### 2. Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Start the NEXUS API

```powershell
cd server
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API can now be tested locally at:

* `http://127.0.0.1:8000`
* `http://127.0.0.1:8000/status`
* `http://127.0.0.1:8000/docs`

**Network note:** Binding to `0.0.0.0` allows the development server to listen on its network interfaces. Only run the development server on trusted networks, and configure appropriate access controls before exposing it to other networks.

### 5. Start the Nico Terminal Client

Open a second PowerShell terminal from the repository root:

```powershell
cd client
python -m http.server 8080 --bind 0.0.0.0
```

Open the client on the development laptop:

`http://127.0.0.1:8080`

To access it from the Vivo Y95, use the development laptop's current LAN IP address:

`http://<LAPTOP-IP>:8080`

**Configuration note:** The current client contains the development server's LAN IP address in its API request URL. Update that address if the laptop's IP changes.

The API and client servers must both be running for the complete text-command interaction to work.

## Development Roadmap

### Phase 1 — Network Foundation

* [x] Connect the Vivo Y95 and development laptop over the home network.
* [x] Verify network connectivity.
* [x] Verify HTTP communication between devices.

### Phase 2 — NEXUS Server and Terminal

* [x] Create the project structure.
* [x] Configure the Python environment and dependencies.
* [x] Implement the FastAPI application.
* [x] Implement the basic API endpoints.
* [x] Create the initial HTML client.
* [x] Establish client-to-server command communication.
* [x] Implement the initial command processor.
* [x] Introduce structured command results, aliases, and command categories.
* [x] Complete end-to-end regression testing of Command System v2.
* [x] Refine API error handling and input validation.

### Phase 3 — Core Architecture

* [x] Separate device management from command interpretation.
* [ ] Define a consistent interface for device integrations.
* [ ] Implement simulated device handlers for development and testing.
* [ ] Improve command routing and execution-result reporting.

### Phase 4 — Device Integrations

* [ ] Investigate and implement compatible Mi Home TV control.
* [ ] Investigate EZVIZ camera integration.
* [ ] Add device-state reporting where supported.
* [ ] Test device actions and error handling.

### Phase 5 — Voice Interaction

* [ ] Evaluate speech-to-text options.
* [ ] Evaluate text-to-speech options.
* [ ] Add voice input and spoken responses.
* [ ] Investigate wake-word detection.

### Phase 6 — Intelligence and Automation

* [ ] Improve natural-language command interpretation.
* [ ] Support configurable routines and automations.
* [ ] Explore local AI integration.
* [ ] Add appropriate permissions and safeguards for device actions.

### Phase 7 — Always-On Deployment

* [ ] Evaluate dedicated local server hardware.
* [ ] Configure reliable startup and recovery.
* [ ] Improve network security and access control.
* [ ] Reduce dependence on the development laptop.

## Design Principles

NEXUS is being developed around the following principles:

* **Modularity:** Keep the API, command processing, and device integrations separate.
* **Incremental development:** Implement and test capabilities before adding more complexity.
* **Transparency:** Distinguish recognized commands from actions actually executed.
* **Local-first exploration:** Prefer evaluating local processing and control options where practical.
* **Maintainability:** Keep the architecture understandable and extensible.
* **Learning by building:** Document technical decisions and develop each component with an understanding of its purpose.

# Author
Aditya

**NEXUS is an ongoing personal software engineering project.**
