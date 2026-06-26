# Subdivision Marketplace — Project Reference

## Overview
A mobile-first Django web app where subdivision sellers post daily products and customers browse today's offerings by category, then contact sellers directly via Messenger/phone.

## Tech Stack
- **Backend:** Django 4.2 + SQLite
- **Frontend:** Django templates + Bootstrap 5 + custom CSS
- **Fonts:** DM Serif Display (headings), DM Sans (body) — Google Fonts
- **Icons:** Bootstrap Icons
- **Images:** `ImageField` with local `media/` fallback (dev) or Cloudinary (production via `CLOUDINARY_URL` env var)

## Data Models

### Category
Pre-defined, manageable via admin. 7 categories seeded: Meals/Ulam, Snacks/Desserts, Drinks & Beverages, Bread/Pastries, Frozen & Ready-to-Cook, Groceries, Services, Palengke.

### Seller (extends AbstractUser)
Custom user model. Fields: `store_name`, `description`, `contact_messenger` (URL), `contact_phone`, `banner_color` (hex), `subscription_notes`.
- `is_active` = subscription toggle. When `False`, products hidden, seller can't log in.
- Accounts created via admin only (invite-only registration).

### Product
Persistent catalog items. Fields: `seller` (FK), `category` (FK), `name`, `description`, `price` (Decimal), `image` (URL), `created_at`.

### DailyProduct
Lightweight availability — one row per product per date. `unique_together = ["product", "date"]`. Customer-facing queries filter by today's date.

## Public Routes (no login)

| Route | Template | Description |
|-------|----------|-------------|
| `/` | `home.html` | Today's products grouped by category, scrollable category pills |
| `/category/<slug>/` | `category.html` | Products filtered by one category |
| `/seller/<id>/` | `seller_detail.html` | Seller store with banner, contact buttons, today's products. Shows "temporarily unavailable" if inactive |
| `/product/<id>/` | `product_detail.html` | Product detail, seller info, Messenger/Call buttons. 404 if seller is inactive |

## Seller Routes (login required)

| Route | Template | Description |
|-------|----------|-------------|
| `/login/` | `login.html` | Email/password login |
| `/logout/` | — | Logout, redirects to `/` |
| `/dashboard/` | `dashboard.html` | Today's Menu — toggle products on/off, see other products |
| `/dashboard/products/` | `product_list.html` | Full product catalog with edit/delete |
| `/dashboard/products/add/` | `product_form.html` | New product form |
| `/dashboard/products/<id>/edit/` | `product_form.html` | Edit product |
| `/dashboard/products/<id>/delete/` | `product_confirm_delete.html` | Delete confirmation |
| `/dashboard/toggle/<product_id>/` | — | POST-only. Adds/removes product from today's menu |
| `/dashboard/settings/` | `settings.html` | Update store name, contact info, banner color |

## Admin Routes

| Route | Description |
|-------|-------------|
| `/admin/` | Django admin — manage sellers, categories, products, DailyProduct entries |

## Seller Daily Workflow
1. Login → Dashboard shows yesterday's products with toggle buttons
2. Tap **"Add to Today"** on products still available
3. Tap **"Remove"** on products sold out
4. Tap **"New Product"** for anything new
5. Done — products appear on public pages for today only

## Subscription / Monetization
- `Seller.is_active` controls store visibility
- Admin unchecks **Active** in `/admin/` to disable a seller (non-payment)
- Disabled seller's products hidden from home/category/seller/product pages
- Disabled seller sees red banner on dashboard
- `subscription_notes` field for tracking payment info (collapsible in admin)

## Design System
- **Primary:** Orange (`#f97316`) with warm gradient nav
- **Accent:** Teal (`#0d9488`) for Messenger buttons
- **Background:** Warm off-white (`#faf5ef`)
- **Text:** Warm brown (`#3d2c1f`)
- **Cards:** White, 16px radius, soft shadows, 4:3 image aspect ratio
- **Animations:** `fadeInUp` with staggered delays on cards

## Deployment
- **Host:** PythonAnywhere (free tier)
- **Commands:** `python manage.py setup_production` for setup steps
- **Env vars:** DJANGO_SECRET_KEY, DJANGO_DEBUG, DJANGO_ALLOWED_HOSTS, DJANGO_CSRF_TRUSTED_ORIGINS
- **Static files:** `collectstatic --noinput` → served from `/static/` URL
- **See:** `DEPLOY.md` for full instructions

## Build Status (all complete)
1. Project scaffold + models + admin
2. Auth + seller dashboard with daily toggle
3. Public pages (customer-facing)
4. Design polish (fonts, colors, animations)
5. Production config + deployment guide

## Superuser (local dev)
- Username: `admin`
- Password: `admin123`

## Git
Project is git-initialized. `.gitignore` excludes `__pycache__`, `*.sqlite3`, `staticfiles/`, `.env`.

## Key Files
```
marketplace/settings.py          — App config, env vars, security
marketplace/urls.py              — Root URL conf (includes sellers.urls)
marketplace/wsgi.py              — WSGI with sys.path for PythonAnywhere
sellers/models.py                — 4 models (Category, Seller, Product, DailyProduct)
sellers/views.py                 — 12 views (public + auth + dashboard)
sellers/urls.py                  — 13 routes
sellers/admin.py                 — Admin registration with subscription management
sellers/forms.py                 — 3 forms (Product, SellerSettings)
sellers/templates/sellers/       — 10 templates
sellers/management/commands/     — setup_production helper
DEPLOY.md                        — Deployment instructions
```
