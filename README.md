# Wooden

**Final Product:** [Play Wooden!](https://wooden-548b2eb943b9.herokuapp.com/)

**Development progress:** [Closed PRs by @DanielOnGitHub17](https://github.com/DanielOnGitHub17/wooden/pulls?q=is%3Apr+is%3Aclosed+author%3ADanielOnGitHub17)

---

## Overview
Wooden is a simple yet competitive two-dimensional multiplayer game where players navigate a maze made of sand, wood, and concrete. The goal? Break the most blocks to claim victory! Wooden emphasizes real-time gameplay with customizable settings for maximum fun.

---

## How to Play
- Use the **arrow keys** to navigate the maze and break blocks.
- Break as many blocks as possible to win.
- You can customize:
    - The **number of players**.
    - The **strength of wood** for each round.

**Play on a laptop or desktop device with a keyboard**
**Phone control coming soon!**

---

## Development
Wooden is powered by a robust backend and an engaging frontend:
- **Backend**: Built on Django, utilizing Channels and real-time websocket communication.
- **Frontend**: Crafted with Django templates, Vanilla CSS, and native JavaScript.
- The system design ensures a seamless, interactive multiplayer experience.

---

## Project structure
This repository is organized around Django backend apps, frontend templates, and static web app assets.

### Backend
- `chat` — Real-time chat service for authenticated players.
  - Handles websocket connections via Django Channels.
  - Broadcasts chat messages to all connected users.
  - Rendered at the in-game chat page.
  - See `chat/README.md`.

- `game` — Core multiplayer game engine and state management.
  - Defines `Game` and `Player` models, game lifecycle, matchmaking, and play logic.
  - Supports creation, joining, leaving, starting, and ending games.
  - Contains maze generation, player positioning, and practice mode.
  - See `game/README.md`.

- `homepage` — Landing pages, help, and support flows.
  - Renders the public landing page, game help page, support contact page, and developer info.
  - Sends support emails to the development team.
  - See `homepage/README.md`.

- `lounge` — Lobby and match creation.
  - Provides the game lounge where players create and join public matches.
  - Uses a `GameForm` to configure new game sessions.
  - Lists available public games and active online players.
  - See `lounge/README.md`.

- `register` — User authentication and registration.
  - Handles quick sign-in, full sign-up, login, logout, account confirmation, and password reset.
  - Supports temporary guest players and reCAPTCHA validation.
  - Sends activation and email verification flows.
  - See `register/README.md`.

### Frontend
#### Templates
- `templates/base.html` — site-wide layout for public and account pages.
  - Includes global navigation, header links, and page metadata.
  - Loads common styles and the shared `static/scripts.js` module.
  - Exposes `{% block title %}` and `{% block content %}` for page-specific content.
- `templates/app.html` — specialized game shell for in-game pages.
  - Wraps the game UI with in-game menu and online player widgets.
  - Includes `app/menu.html` and `app/online.html` partials.
  - Provides a fullscreen game entry flow and a dedicated `#APP` render container.
- `templates/messages.html` — site-wide messaging component for Django messages.
- App templates under `templates/app/` drive lounge, chat, and game views.
- `templates/homepage/`, `templates/registration/`, and other paths contain the public pages served by the Django backend.

#### Web App
- `static/scripts.js` — global frontend bootstrap and shared DOM event wiring.
  - Sets common handlers for navigation, menu toggles, messages, and keyboard shortcuts.
  - Exposes `username` and utility helpers used by app-specific modules.
- `static/game/` — core browser game client.
  - `game.js` orchestrates the game grid, block rendering, player creation, and game state transitions.
  - `socket.js` manages `GameSocket` for backend websocket communication at `/ws/game/<game_id>/`.
  - `events.js` wires page lifecycle events, multiplayer initialization, fetch calls for server actions, and websocket event callbacks.
  - Other modules such as `player.js`, `bot.js`, `gamer.js`, `block.js`, and `sound.js` encapsulate player behavior, AI opponents, game entities, and audio playback.
  - The client updates game state locally and reacts to server-sent events for player movement, game start, and lobby changes.
- `static/chat/` — chat UI and websocket messaging.
  - `chat.js` renders chat bubbles, sends messages over `/ws/chat/`, and receives broadcasted chat data.
  - `events.js` in the chat folder handles chat form submission and socket lifecycle events.
- `static/lounge/` and `static/register/` — page-specific frontend assets for lobby and auth flows.
  - These folders contain styles and scripts tied to lobby and registration pages.

Frontend static folder docs:
- `static/chat/README.md`
- `static/game/README.md`
- `static/lounge/README.md`
- `static/register/README.md`

### Shared utilities
- `helpers.py` — Common backend helpers for email creation, websocket authentication, group messaging, reCAPTCHA verification, and custom error handling.
- `wooden/` — Django project package containing `asgi.py`, `settings.py`, `urls.py`, and `wsgi.py`.

### Additional repo assets
- `metrics/` — Static asset folder containing latency and performance charts.
- `static/` and `templates/` — Frontend assets and HTML templates used across the project.

---

## Deployment and tooling
### Gunicorn
- `gunicorn.conf.py` provides Heroku-ready Gunicorn settings.
- Key settings:
  - binds to `PORT` and supports IPv6 via `[::]:${PORT}`.
  - uses `gthread` worker class with `threads = 5`.
  - `workers` is controlled by `WEB_CONCURRENCY`, defaulting to `1`.
  - enables `preload_app`, `timeout = 20`, and `graceful_timeout = 20`.

### Process files
- `Procfile` — production command: `python -m gunicorn wooden.asgi:application -k uvicorn.workers.UvicornWorker`.
- `Procfile.windows` — local Windows command: `python manage.py runserver %PORT%`.

### Scripts
- `scripts/deploy.bat` — Windows deployment helper.
- `scripts/merge_dependabot_prs.sh` and `scripts/reroute_dependabot_prs.sh` — automation for Dependabot PR management.
- `scripts/merge_prs.bat` and `scripts/reroute_dependabot_prs.bat` — Windows equivalents for PR automation.

### Git hooks
- `.githooks/pre-push` — pre-push checks that block a push if:
  - migrations are not up to date (`python manage.py makemigrations --check`).
  - tests fail (`python manage.py test`).
  - requirements cannot be installed (`python -m pip install -r requirements.txt --require-virtualenv`).
- Enable hooks with `git config core.hooksPath .githooks`.

---

## Developers

#### **Andrew Emeghebo** and **Daniel Enesi**
- Computer Science majors at **Grambling State University**, currently rising seniors.
- Passionate about web development:
    - **Daniel** thrives in backend logic and architecture.
    - **Andrew** excels in designing responsive, intuitive user interfaces.

---

## License
This project is open-source. Please adhere to the licensing terms when using or modifying Wooden.

Enjoy!
Break blocks, battle it out, and immerse yourself in the fun of Wooden!
