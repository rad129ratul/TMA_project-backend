# TMA_project-backend

Django + Django REST Framework backend powering a **Task Management (Kanban)** module
and an **Image Annotation** module, unified under a single JWT-authenticated API.

**Live API:** `https://tma-project-backend.onrender.com/admin/`
**Frontend Repo:** `https://github.com/rad129ratul/TMA_project-frontend`

---

## Tech Stack

| Component | Choice |
|---|---|
| Language | Python 3.10+ |
| Framework | Django 6.0.6 + Django REST Framework 3.17.1 |
| Auth | djangorestframework-simplejwt (JWT, access + refresh) |
| Database | SQLite (dev & demo) |
| Image handling | Pillow |
| Production server | Gunicorn |
| Static files | WhiteNoise |
| CORS | django-cors-headers |

---

## Prerequisites

- Python **3.10 or higher** (`python --version`)
- pip + venv (bundled with Python)
- Git

---

## Local Setup — Step by Step

```bash
# 1. Clone the repo
git clone https://github.com/rad129ratul/TMA_project-backend.git
cd TMA_project-backend

# 2. Create and activate a virtual environment
python -m venv venv
Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables (see table below)
cp .env.example .env            # then fill in the values

# 5. Run migrations
python manage.py migrate

# 6. Create a superuser (for Django admin access)
python manage.py createsuperuser

# 7. Start the dev server
python manage.py runserver
```

Backend will be running at `http://127.0.0.1:8000`.

---

## Environment Variables

Create a `.env` file in the project root with the following keys:

```env
SECRET_KEY=django-insecure-replace-this-with-a-real-random-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

> Generate a real `SECRET_KEY` with:
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

**Production values** (set these in the Render dashboard, not in a committed file):

```env
SECRET_KEY=<a separate, real random secret — never reuse the dev key>
DEBUG=False
ALLOWED_HOSTS=<your-backend>.onrender.com
CORS_ALLOWED_ORIGINS=https://<your-frontend>.vercel.app
```

---

## API Documentation

### Authentication

| Method | Path | Auth Required | Body | Response |
|---|---|---|---|---|
| POST | `/api/auth/login/` | No | `{ "username", "password" }` | `{ "access", "refresh" }` |
| POST | `/api/auth/refresh/` | No | `{ "refresh" }` | `{ "access" }` |
| GET | `/api/accounts/ping/` | Yes (Bearer) | — | `{ "message": "pong", "user" }` |

### Tasks

| Method | Path | Auth Required | Body | Response |
|---|---|---|---|---|
| GET | `/api/tasks/` | Yes | — | List of the logged-in user's tasks |
| GET | `/api/tasks/?date=YYYY-MM-DD` | Yes | — | Tasks filtered by `due_date` |
| POST | `/api/tasks/` | Yes | `{ title, priority, due_date, tags, status }` | Created task |
| GET | `/api/tasks/<id>/` | Yes | — | Single task |
| PATCH | `/api/tasks/<id>/` | Yes | Any subset of task fields | Updated task |
| DELETE | `/api/tasks/<id>/` | Yes | — | `204 No Content` |

### Images & Annotations

| Method | Path | Auth Required | Body | Response |
|---|---|---|---|---|
| GET | `/api/annotations/images/?task=<id>` | Yes | — | Images belonging to that task |
| POST | `/api/annotations/images/` | Yes | `multipart/form-data: { file, task }` | Created image |
| GET | `/api/annotations/annotations/?image=<id>` | Yes | — | Annotations for that image |
| POST | `/api/annotations/annotations/` | Yes | `{ image, points: [{x,y}...], label }` | Created annotation |
| PATCH | `/api/annotations/annotations/<id>/` | Yes | `{ label }` | Updated annotation |
| DELETE | `/api/annotations/annotations/<id>/` | Yes | — | `204 No Content` |

All endpoints except `/api/auth/*` require an `Authorization: Bearer <access_token>` header.

---

## Data Model Overview
User
└── Task (owner FK)
└── UploadedImage (task FK, one-to-many)
└── Annotation (image FK, one-to-many)

- `Task → UploadedImage → Annotation` forms a fully cascading delete chain —
  deleting a Task removes its images, which removes their annotations. No orphan records.

---

## Deployment (Render)

- **Build Command:** `./build.sh`
- **Start Command:** `gunicorn core.wsgi:application --bind 0.0.0.0:$PORT`
- Environment variables set via the Render dashboard (see table above)

---

## Difficulties Faced & Solutions

### 1. `on_delete=CASCADE` vs `SET_NULL` — Image → Annotation relationship

**The problem:** When designing the `Annotation` model, we had to decide what should
happen to an `Annotation` record if its parent `UploadedImage` is deleted.

**Why `CASCADE` was the right choice:** An `Annotation` is fundamentally an
**existential dependency** on its `UploadedImage` — a set of `(x, y)` polygon points
has no meaning without knowing which image they were drawn on. If we had used
`SET_NULL`, deleting an image would leave behind orphan `Annotation` rows with a null
`image` field — records that can never be rendered (no image to draw them on), would
still occupy database space, and would require defensive null-checks everywhere they're
queried. `SET_NULL` only makes sense when the child entity can meaningfully exist
without its parent (e.g. keeping a `Task`'s history even if its `owner` user is
deleted) — that is not the case here. `CASCADE` keeps the database orphan-free by
construction, not by convention.

### 2. Production CORS failures after deployment

**The problem:** After deploying the backend to Render and the frontend to Vercel,
API calls from the live frontend were blocked with a CORS error, even though the same
code worked flawlessly in local development.

**Root cause:** In local dev, `CORS_ALLOWED_ORIGINS` was hardcoded to
`http://localhost:3000`. Once frontend and backend moved to two completely different
production domains, that hardcoded value no longer matched — the browser correctly
blocked the cross-origin request.

**The fix:** `CORS_ALLOWED_ORIGINS` and `ALLOWED_HOSTS` were converted to be
environment-variable-driven (using `python-decouple`'s `Csv()` cast), so the same
codebase behaves correctly in both dev and prod — only the environment variable value
changes, not the code. We also learned the hard way that a trailing slash difference
(`https://myapp.vercel.app/` vs `https://myapp.vercel.app`) causes an exact-match
failure in `CORS_ALLOWED_ORIGINS`, and that Render does **not** automatically redeploy
on environment variable changes — a manual redeploy is required for the new value to
take effect.

---

## Demo Credentials

- **Email:** `ratul@gmail.com`
- **Password:** `test1234#@`