Thought for a second

````markdown
# Jam-Date

A full-stack dating application built with **Flask** (Python) on the backend and **Vue 3** on the frontend. Users can register, maintain up to three distinct “profiles” (each with its own photo and preferences), browse the most recent profiles, search by multiple criteria, and click **Match Me** to discover compatible matches based on age, height, and shared interests.

---

## Features

- **User Authentication** (JWT-based)
- **Profile Management**
  - Each user may create up to **3** profiles
  - Upload a unique photo per profile
- **Latest Profiles Feed** (4 most recently created)
- **Server-Side Search** by:
  - Name
  - Birth Year
  - Sex
  - Race
- **Match Me Algorithm**
  1. Age difference ≤ 5 years
  2. Height difference between 3 – 10 inches
  3. At least 3 of 6 preference fields match:  
     `fav_cuisine`, `fav_colour`, `fav_school_subject`, `political`, `religious`, `family_oriented`
- **Favorites Report**
  - View top-favorited profiles
  - Manage your personal favorites
- **Deployed on Render.com** with managed PostgreSQL, Flask Web Service, and Vue Static Site

---

## 🛠 Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-WTForms, Flask-CORS
- **Database**: PostgreSQL
- **Frontend**: Vue 3, Vue Router, Axios, Vite, Bootstrap 5
- **Deployment**: Render.com

---

## Quickstart

### 1. Clone repository

```bash
git clone https://github.com/your-org/jam-date.git
cd jam-date
```
````

### 2. Backend setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Copy and edit env file:
cp .env.sample .env
# └ define SECRET_KEY, DATABASE_URL (postgres://…), FRONTEND_URL

# Initialize database schema:
flask db upgrade

# Run development server:
flask run
```

API is now at `http://127.0.0.1:5000/api/...`

### 3. Frontend setup

```bash
cd ../frontend
npm install

# Copy and edit env file:
cp .env.sample .env
# └ define VITE_API_BASE_URL=http://127.0.0.1:5000

npm run dev
```

Open `http://localhost:5173` in your browser.

---

## ⚙️ Environment Variables

#### Backend (`backend/.env`)

```ini
SECRET_KEY=your_flask_secret
DATABASE_URL=postgresql://user:pass@host:5432/dbname
FRONTEND_URL=http://localhost:5173
```

#### Frontend (`frontend/.env`)

```ini
VITE_API_BASE_URL=http://127.0.0.1:5000
```

---

## Database Migrations

Whenever you change your models:

```bash
cd backend
flask db migrate -m "Describe changes"
flask db upgrade
```

---

## 📡 Deployment on Render

1. **PostgreSQL**

   - Create a managed PostgreSQL instance.
   - Copy the **Internal Database URL**.

2. **Flask Web Service**

   - Connect backend repo.
   - Build Command:

     ```bash
     pip install -r requirements.txt && flask db upgrade
     ```

   - Start Command:

     ```
     gunicorn app:app
     ```

   - Environment Variables: `SECRET_KEY`, `DATABASE_URL` (internal), `FRONTEND_URL`

3. **Vue Static Site**

   - Connect frontend repo.
   - Build Command:

     ```
     npm install && npm run build
     ```

   - Publish Directory: `dist`
   - Environment Variable: `VITE_API_BASE_URL` = your Flask service URL

Render will automatically build and deploy on each push.

---

## 🔗 API Reference

| Method | Endpoint                                   | Description                             |
| ------ | ------------------------------------------ | --------------------------------------- |
| POST   | `/api/register`                            | Register a new user                     |
| POST   | `/api/auth/login`                          | Log in (returns JWT & user_id)          |
| GET    | `/api/csrf-token`                          | Fetch CSRF token                        |
| POST   | `/api/users/<id>/photo`                    | Upload a user’s profile photo           |
| GET    | `/api/uploads/<filename>`                  | Serve uploaded photo                    |
| GET    | `/api/users/<id>`                          | Get user details & their profiles       |
| GET    | `/api/profiles?limit=N`                    | List latest N profiles (excluding self) |
| POST   | `/api/profiles`                            | Create a new profile                    |
| GET    | `/api/profiles/<id>`                       | Get profile details                     |
| GET    | `/api/profiles/matches/<id>`               | Get matches for a profile               |
| GET    | `/api/search?name=&sex=&race=&birth_year=` | Search profiles                         |
| GET    | `/api/users/<id>/favourites`               | Get your favourites                     |
| GET    | `/api/users/favourites/<N>`                | Get top-N favourited profiles           |
| POST   | `/api/profiles/<id>/favourite`             | Add a profile to your favourites        |

---

## License

This project is licensed under **MIT**. See [LICENSE](LICENSE) for details.

---

❤️ Happy matching!

```

```
