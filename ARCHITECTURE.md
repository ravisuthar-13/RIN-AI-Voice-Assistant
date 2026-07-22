# 🏗 RIN Project Architecture

This document explains the internal architecture of the RIN AI Voice Assistant.

RIN uses a modular Python architecture so that voice processing, command detection, system controls, application launching, and future AI features can be developed independently.

---

## 🔄 Command Processing Flow

```text
User Voice
    │
    ▼
Speech Recognition
    │
    ▼
main.py
    │
    ▼
Command Normalization
    │
    ▼
Natural Language Conversion
    │
    ▼
commands.py
    │
    ▼
CommandResult
    │
    ├── Response Text
    ├── Optional Action
    └── Exit Status
    │
    ▼
Application / Website / Folder / System Action
```

---

## 🧠 Core Architecture

```text
┌──────────────────────────────┐
│          User Voice          │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│     Speech Recognition       │
│ SpeechRecognition + Google   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│           main.py            │
│ Listening, speaking and loop │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│         commands.py          │
│ Normalize, detect and route  │
└──────────────┬───────────────┘
               │
     ┌─────────┼──────────┬───────────┐
     │         │          │           │
     ▼         ▼          ▼           ▼
┌─────────┐ ┌──────────┐ ┌─────────┐ ┌────────────────┐
│ apps.py │ │websites.py│ │folders.py│ │system modules │
└─────────┘ └──────────┘ └─────────┘ └────────────────┘
                                           │
                         ┌─────────────────┴─────────────────┐
                         ▼                                   ▼
                ┌────────────────┐                  ┌──────────────────┐
                │ system_info.py │                  │system_controls.py│
                └────────────────┘                  └──────────────────┘
```

---

## 📁 Main Files

| File | Responsibility |
|------|----------------|
| `main.py` | Starts RIN, listens to the user, speaks responses and executes actions |
| `commands.py` | Normalizes commands, detects user intent and routes commands |
| `config.py` | Stores global configuration, voice settings and default responses |
| `data.py` | Stores supported applications, websites, folders and command aliases |
| `apps.py` | Opens Windows applications |
| `websites.py` | Opens supported websites |
| `folders.py` | Opens configured folders |
| `system_info.py` | Provides battery, CPU, RAM and disk information |
| `system_controls.py` | Handles volume, brightness and media controls |

---

## 📦 CommandResult Structure

The command engine returns a structured `CommandResult` object.

```python
@dataclass
class CommandResult:
    response: str
    should_exit: bool = False
    action: Optional[Callable[[], None]] = None
```

### Fields

- `response` — Text spoken by RIN
- `should_exit` — Tells the main loop to stop
- `action` — Optional function executed after RIN speaks

This design keeps command detection separate from command execution.

---

## 🗂 Development Workflow

RIN uses two separate folders.

### Development Workspace

```text
RIN/
```

Used for:

- New feature development
- Experiments
- Testing
- Debugging
- Version backups
- Temporary scripts

### Stable GitHub Repository

```text
RIN-AI-Voice-Assistant/
```

Used for:

- Stable source code
- Clean project structure
- Documentation
- GitHub releases
- Portfolio presentation

### Release Flow

```text
Development Workspace
        │
        ▼
Feature Development
        │
        ▼
Command Testing
        │
        ▼
Voice Integration Testing
        │
        ▼
Bug Fixing
        │
        ▼
Stable Version
        │
        ▼
Copy Clean Files to GitHub Repository
        │
        ▼
Git Commit and Git Push
```

---

## 🚀 Current Architecture Status

| Component | Status |
|-----------|--------|
| Voice Input | ✅ Working |
| Text-to-Speech | ✅ Working |
| Smart Command Engine | ✅ Working |
| Natural Language Preprocessing | ✅ Working |
| App Launcher | ✅ Working |
| Website Launcher | ✅ Working |
| Folder Launcher | ✅ Working |
| System Monitoring | ✅ Working |
| System Controls | ✅ Working |
| Wikipedia Search | ⚠ Under Improvement |
| Personal Memory System | 🚧 Planned for v3.1 |
| AI Conversation Layer | ⏳ Future |

---

## 🔮 Planned Architecture

RIN v3.1 will introduce a persistent memory layer.

```text
User Command
     │
     ▼
Command Engine
     │
     ▼
Memory Manager
     │
     ├── Save Information
     ├── Recall Information
     ├── Update Information
     └── Delete Information
     │
     ▼
JSON Memory Storage
```

Future versions may add:

```text
Voice
  ↓
Command Engine
  ↓
Intent Detection
  ↓
Memory System
  ↓
AI Conversation Engine
  ↓
Automation Engine
  ↓
Desktop Actions
```

---

## 👨‍💻 Author

**Ravi Suthar**

RIN is a personal AI assistant project built to learn Python, AI, automation, voice interaction and software architecture through practical development.
