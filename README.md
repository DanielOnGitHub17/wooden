# Wooden

**Final Product:** [Play Wooden!](https://wooden-548b2eb943b9.herokuapp.com/)

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

**Best played on a laptop for optimal experience!**

---

## Development
Wooden is powered by a robust backend and an engaging frontend:
- **Backend**: Built on Django, utilizing Channels and Redis for real-time functionality.
- **Frontend**: Crafted with Django's Jinja2-like Template Language, Vanilla CSS, and native JavaScript.
- The system design ensures a seamless, interactive multiplayer experience.

---

## Developers

#### **Andrew Emeghebo** and **Daniel Enesi**
- Computer Science majors at **Grambling State University**, currently sophomores.
- Passionate about web development:
    - **Daniel** thrives in backend logic and architecture.
    - **Andrew** excels in designing responsive, intuitive user interfaces.

---

## Contributing
We welcome contributions to Wooden! Here's how you can contribute:
- **Issues**: Feel free to open issues for suggestions, bug reports, or enhancements. Please note that all issues must be **approved by maintainers** before being addressed.
- **Pull Requests**: Contributors can open pull requests after they have been approved by the maintainers. Thank you for your understanding!

---

## Deployment
The live version of Wooden can be accessed here: **[https://playwooden.games/](https://playwooden.games/)**

To run Wooden locally:
1. Clone the repository.
2. Install dependencies from `requirements.txt`.
3. Run migrations and start the server:

```bash
python manage.py migrate
python manage.py runserver
```

Access the application at http://127.0.0.1:8000/.

For production, a WSGI server like Gunicorn is recommended.

---

## License
This project is open-source. Please adhere to the licensing terms when using or modifying Wooden.

Enjoy!
Break blocks, battle it out, and immerse yourself in the fun of Wooden!