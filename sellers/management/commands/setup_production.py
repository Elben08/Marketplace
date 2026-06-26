from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    help = "Prepare project for production deployment"

    def handle(self, *args, **options):
        secret_key = get_random_string(50, "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)")

        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write(self.style.SUCCESS("  SUBDIVISION MARKETPLACE — DEPLOYMENT SETUP"))
        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write("")
        self.stdout.write("1. Generate a Django SECRET_KEY:")
        self.stdout.write(self.style.NOTICE(f"   {secret_key}"))
        self.stdout.write("")
        self.stdout.write("2. Run migrations:")
        self.stdout.write(self.style.WARNING("   python manage.py migrate"))
        self.stdout.write("")
        self.stdout.write("3. Collect static files:")
        self.stdout.write(self.style.WARNING("   python manage.py collectstatic --noinput"))
        self.stdout.write("")
        self.stdout.write("4. Create superuser (you):")
        self.stdout.write(self.style.WARNING("   python manage.py createsuperuser"))
        self.stdout.write("")
        self.stdout.write("5. Set these environment variables on PythonAnywhere:")
        self.stdout.write("   (Web tab -> Environment variables)")
        self.stdout.write("")
        self.stdout.write(f"   DJANGO_SECRET_KEY={secret_key}")
        self.stdout.write("   DJANGO_DEBUG=False")
        self.stdout.write("   DJANGO_ALLOWED_HOSTS=yourusername.pythonanywhere.com")
        self.stdout.write("   DJANGO_CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com")
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Done! Ready for deployment."))
