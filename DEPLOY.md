# Deployment Guide — PythonAnywhere

## 1. Create a PythonAnywhere account

Sign up at https://www.pythonanywhere.com (free tier is sufficient).

## 2. Upload the project

**Option A — Git (recommended):**
```bash
# On your local machine:
cd C:\Users\1000332504\Documents\opencode\Marketplace
git init
git add .
git commit -m "Initial commit"
# Create a repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/marketplace.git
git push -u origin main

# On PythonAnywhere (Bash console):
git clone https://github.com/YOUR_USERNAME/marketplace.git
```

**Option B — Zip upload:**
1. Zip the project folder (exclude `__pycache__`, `*.sqlite3`, `.git/`)
2. Upload via PythonAnywhere Files tab
3. Unzip in the console: `unzip marketplace.zip`

## 3. Set up virtualenv and install dependencies

```bash
cd marketplace
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 4. Configure the web app

1. Go to **Web** tab in PythonAnywhere
2. Click **Add a new web app**
3. Choose **Manual configuration** → Python 3.8
4. Set:
   - **Source code:** `/home/YOUR_USERNAME/marketplace`
   - **Working directory:** `/home/YOUR_USERNAME/marketplace`
   - **Virtualenv:** `/home/YOUR_USERNAME/marketplace/venv`
   - **WSGI file:** click it — it should already point to `/home/YOUR_USERNAME/marketplace/marketplace/wsgi.py`

   The WSGI file already has `python-dotenv` loading code, so no manual editing needed.

## 5. Set environment variables

The WSGI file automatically loads a `.env` file from the project root. Create it:

```bash
cd ~/marketplace

# Generate a secret key
python manage.py setup_production

# OR generate one manually:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"  

# Create the .env file (replace values as needed):
echo 'export DJANGO_SECRET_KEY=(!w!rmywoj#-*jnvdkzi_7wly+ztz$l4p^&em32&x#of2ll#+d' >> .env
echo "export DJANGO_DEBUG=False" >> .env
echo "export DJANGO_ALLOWED_HOSTS=elben.pythonanywhere.com" >> .env
echo "export DJANGO_CSRF_TRUSTED_ORIGINS=https://elben.pythonanywhere.com" >> .env

# Optional — enable Cloudinary image uploads:
# echo "CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME" >> .env
```

## 6. Set up static files

In the **Web** tab, under **Static files**:
- **URL:** `/static/`
- **Path:** `/home/YOUR_USERNAME/marketplace/staticfiles`

Then in the Bash console:
```bash
cd marketplace
source venv/bin/activate
python manage.py collectstatic --noinput
```

## 7. Run migrations and create admin

```bash
python manage.py migrate
python manage.py createsuperuser
```

## 8. Reload

Click the **Reload** button in the Web tab.

Your site is live at `https://YOUR_USERNAME.pythonanywhere.com` 🎉

## 9. Create seller accounts

1. Visit `https://YOUR_USERNAME.pythonanywhere.com/admin/`
2. Log in with your superuser credentials
3. Under **Sellers**, click **Add** to create seller accounts
4. Give each seller their login credentials

## Updating the site

```bash
git pull                          # get latest code
source venv/bin/activate          # activate venv
pip install -r requirements.txt   # update deps
python manage.py migrate          # run migrations
python manage.py collectstatic --noinput  # update static files
# Then click Reload in the Web tab
```
