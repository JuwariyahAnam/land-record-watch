"""Admin commands.
  python -m src.portal.admin create-registrar you@example.com "Demo Registrar"
  python -m src.portal.admin seed-demo
The registrar is the only role that can approve or reject changes. Passwords are asked for here and never printed."""
import getpass
import sys

from . import security as sec
from . import store


def create(email, name, role):
    pw = getpass.getpass("Password (min 10 characters, letters and numbers): ")
    problem = sec.password_problem(pw, email, name)
    if problem:
        raise SystemExit(problem)
    if pw != getpass.getpass("Repeat password: "):
        raise SystemExit("passwords do not match")
    db = store.conn()
    if store.user_by_email(db, email.lower()):
        raise SystemExit("that email already exists")
    store.create_user(db, email.lower(), name, role, sec.hash_password(pw))
    print(f"created {role}: {email}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["create-registrar"] and len(args) == 3:
        create(args[1], args[2], "registrar")
    elif args[:1] == ["seed-demo"]:
        print("Creating a registrar, a landlord and a buyer. Use the same password for all three while testing.")
        create("registrar@demo.example", "Demo Registrar", "registrar")
        create("landlord@demo.example", "Demo Landlord", "landlord")
        create("buyer@demo.example", "Demo Buyer", "buyer")
    else:
        raise SystemExit(__doc__)
