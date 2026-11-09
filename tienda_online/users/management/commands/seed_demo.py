"""Comando para crear los usuarios de prueba de la práctica."""

from django.core.management.base import BaseCommand

from users.models import User

DEMO_USERS = [
    {
        "email": "admin@tiendaonline.com",
        "password": "Admin12345!",
        "first_name": "Administrador",
        "last_name": "Tienda",
        "phone": "5550000001",
        "is_staff": True,
        "is_superuser": True,
    },
    {
        "email": "cliente@tiendaonline.com",
        "password": "Cliente12345!",
        "first_name": "Cliente",
        "last_name": "Demo",
        "phone": "5550009999",
        "is_staff": False,
        "is_superuser": False,
    },
]


class Command(BaseCommand):
    help = "Crea o actualiza los usuarios de prueba (admin y cliente)."

    def handle(self, *args, **options):
        for data in DEMO_USERS:
            email = data["email"]
            password = data["password"]
            defaults = {
                key: value
                for key, value in data.items()
                if key not in ("email", "password")
            }

            user, created = User.objects.get_or_create(
                email=email, defaults=defaults
            )

            # No se sobrescriben datos personales ya editados.
            for field in ("first_name", "last_name", "phone"):
                if not getattr(user, field):
                    setattr(user, field, defaults[field])

            user.is_active = True
            user.is_staff = defaults["is_staff"]
            user.is_superuser = defaults["is_superuser"]
            user.set_password(password)
            user.save()

            action = "creado" if created else "actualizado"
            self.stdout.write(
                self.style.SUCCESS(f"Usuario {action}: {email}")
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Usuarios de prueba listos. "
                "Admin: admin@tiendaonline.com / Admin12345! | "
                "Cliente: cliente@tiendaonline.com / Cliente12345!"
            )
        )
