# Subdivision Marketplace — Project Reference

## Overview
A mobile-first Django web app where subdivision sellers post daily products and customers browse today's offerings by category or by store, then contact sellers directly via Messenger/phone.

## Tech Stack
- **Backend:** Django 4.2 + SQLite
- **Frontend:** Django templates + Bootstrap 5.3.0 (served locally, no CDN) + custom CSS
- **Fonts:** DM Serif Display (headings), DM Sans (body) — Google Fonts
- **Icons:** Bootstrap Icons 1.11.0 (served locally)
- **Images:** `ImageField` with local `media/` fallback (dev/free PythonAnywhere) or Cloudinary (paid, via `CLOUDINARY_URL` env var)
- **Env vars:** Loaded via `python-dotenv` in `settings.py` (no manual `source .env` needed)

## Data Models

### Category
Pre-defined, manageable via admin. 8 categories seeded: Meals/Ulam, Snacks/Desserts, Drinks & Beverages, Bread/Pastries, Frozen & Ready-to-Cook, Groceries, Services, Palengke.

### Seller (extends AbstractUser)
Custom user model. Fields: `store_name`, `description`, `contact_messenger` (URL), `contact_phone`, `banner_color` (hex), `subscription_notes`, `menu_image` (ImageField).
- `is_active` = subscription toggle. When `False`, products hidden, seller can't log in.
- Accounts created via admin only (invite-only registration).
- `menu_image` flyer upload auto-resized to max 1200px width, JPEG @ 85% quality.

### Product
Persistent catalog items. Fields: `seller` (FK), `category` (FK), `name`, `description`, `price` (Decimal), `image` (ImageField), `created_at`.
- `save()` override auto-resizes new uploads to max 1200px width, JPEG @ 85% quality, ~4MB → ~150KB.

### DailyProduct
Lightweight availability — one row per product per date. `unique_together = ["product", "date"]`. Customer-facing queries filter by today's date.

## Public Routes (no login)

| Route | Template | Description |
|-------|----------|-------------|
| `/` | `home.html` | Today's products grouped by category, scrollable category pills |
| `/stores/` | `store_list.html` | All active sellers with today's product previews |
| `/category/<slug>/` | `category.html` | Products filtered by one category |
| `/seller/<id>/` | `seller_detail.html` | Seller store with banner, contact buttons, menu flyer, today's products. Shows "temporarily unavailable" if inactive |
| `/product/<id>/` | `product_detail.html` | Product detail, seller info, Messenger/Call buttons. 404 if seller is inactive |

## Seller Routes (login required)

| Route | Template | Description |
|-------|----------|-------------|
| `/login/` | `login.html` | Email/password login. "Forgot password?" link advises contacting admin |
| `/logout/` | — | Logout, redirects to `/` |
| `/dashboard/` | `dashboard.html` | Today's Menu — toggle products on/off, see other products. Triggers 4-day stale image cleanup (once/day via cache) |
| `/dashboard/products/` | `product_list.html` | Full product catalog with side-by-side edit/delete buttons |
| `/dashboard/products/add/` | `product_form.html` | New product form with `enctype="multipart/form-data"` + `accept="image/*"` |
| `/dashboard/products/<id>/edit/` | `product_form.html` | Edit product |
| `/dashboard/products/<id>/delete/` | `product_confirm_delete.html` | Delete confirmation |
| `/dashboard/toggle/<product_id>/` | — | POST-only. Adds/removes product from today's menu |
| `/dashboard/settings/` | `settings.html` | Update store name, description, menu flyer, contact info, banner color |

## Admin Routes

| Route | Description |
|-------|-------------|
| `/admin/` | Django admin — manage sellers, categories, products, DailyProduct entries. Admin-assisted password reset via seller edit page (built into `UserAdmin`). Admin self-reset via `python manage.py changepassword <username>` |

## Seller Daily Workflow
1. Login → Dashboard shows yesterday's products with toggle buttons
2. Tap **"Add to Today"** on products still available
3. Tap **"Remove"** on products sold out
4. Tap **"New Product"** for anything new — phone gallery opens for image pick
5. Image auto-resized on upload (~4MB → ~150KB)
6. Optionally upload a store menu flyer via **Settings** (once, semi-permanent)
7. Done — products appear on public pages for today only

## Image Handling
- **Upload (products):** Phone gallery picker → `ImageField` with `accept="image/*"` → `Product.save()` resizes to max 1200px width, optimizes as JPEG @ 85% quality.
- **Upload (menu flyer):** Settings page → `Seller.menu_image` → auto-resized same as products.
- **Resize helper:** Shared `_resize_image()` function in `models.py` used by both `Product.save()` and `Seller.save()`.
- **Storage:** Local `media/products/` and `media/menus/` by default. If `CLOUDINARY_URL` env var is set, switches to Cloudinary CDN automatically.
- **Cleanup:** Products not listed in `DailyProduct` for 4+ days get their image deleted. Runs automatically on dashboard visit (rate-limited to once/day via cache) or via `python manage.py cleanup_old_images`.

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
- **Static files:** `collectstatic --noinput` → served from `/static/`
- **Media files:** `/media/` → served from project `media/` directory (add Web tab → Static files)
- **Env vars:** Git-ignored `.env` file loaded automatically by `settings.py` via `python-dotenv`
- **See:** `DEPLOY.md` for full instructions

## Build History
1. Project scaffold + models + admin
2. Auth + seller dashboard with daily toggle
3. Public pages (customer-facing)
4. Design polish (fonts, colors, animations)
5. Production config + deployment guide
6. Category "Others" renamed→ "Services"; added "Palengke" (8 total)
7. Image upload: `URLField` → `ImageField` + Cloudinary/local storage switch
8. Bootstrap & Icons moved from CDN to local vendor files (no proxy blocking)
9. Mobile layout fix: edit/delete buttons now side-by-side on narrow screens
10. Image auto-resize on upload (Pillow, 1200px max, JPEG @ 85%)
11. Stale image cleanup (4 days inactive, auto-run on dashboard + management command)
12. Store listing page (`/stores/`) with seller cards + today's product previews
13. dotenv moved from WSGI to `settings.py` (works for both web app and `manage.py`)
14. Store menu flyer upload — `Seller.menu_image` field, resize on save
15. "Forgot password?" link on login page — admin-assisted reset

## Superuser (local dev)
- Username: `admin`
- Password: `admin123`

## Git
Project is git-initialized. `.gitignore` excludes `__pycache__`, `*.sqlite3`, `staticfiles/`, `.env`.

## Key Files
```
marketplace/settings.py              — App config, dotenv loading, Cloudinary switch, env vars
marketplace/urls.py                  — Root URL conf (includes sellers.urls)
marketplace/wsgi.py                  — WSGI with sys.path for PythonAnywhere
sellers/models.py                    — 4 models + _resize_image() helper + Product/Seller.save() with resize
sellers/views.py                     — 13 views (6 public, 6 auth, 1 dashboard with auto-cleanup)
sellers/urls.py                      — 14 routes
sellers/admin.py                     — Admin registration with subscription management
sellers/forms.py                     — 3 forms (Product with ClearableFileInput, SellerSettings with menu_image)
sellers/templates/sellers/           — 11 templates (incl. store_list, login with forgot pw)
sellers/management/commands/         — setup_production, cleanup_old_images
sellers/static/sellers/vendor/       — Bootstrap 5.3.0 CSS/JS, Icons 1.11.0 (local)
sellers/migrations/                  — 7 migrations (seed, rename, add services, palengke, image, menu)
DEPLOY.md                            — Deployment instructions
.env.example                         — Env var template
```
