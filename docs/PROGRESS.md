# AutoPoster Project Progress

## Module 1 — Project Setup & Auth (Completed)
What was built:
- FastAPI backend with SQLite (dev) / PostgreSQL (prod) via SQLAlchemy
- JWT-based authentication with silent token renewal
- Health check endpoints
- Next.js frontend with Tailwind CSS
- Login screen and guarded dashboard routes
- API client wrapper for seamless JWT handling

## Module 2 — Facebook OAuth Connection (Completed)

What was built:
- FacebookPage database model
- Token encryption (Fernet)
- OAuth connect/callback/select-page/status/disconnect endpoints
- Settings > Facebook frontend page

Environment variables added:
- FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, FACEBOOK_REDIRECT_URI, FACEBOOK_TOKEN_ENCRYPTION_KEY, BACKEND_URL

Setup required by user:
- Create Facebook App (see backend/docs/facebook_setup.md)
- Generate FACEBOOK_TOKEN_ENCRYPTION_KEY
- Add redirect URI to Facebook App settings

How to test:
- Go to /settings/facebook, click Connect Facebook, approve on Facebook, confirm page shows as connected

