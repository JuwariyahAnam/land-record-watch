"""Demo land registry. Three kinds of login: landlord, buyer, registrar.
Fictional data only. This is NOT an official record and does not imitate any government site."""
import os
import hmac
import time
from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import Flask, abort, flash, g, redirect, render_template, request, session, url_for

from . import security as sec
from . import store

IST = timezone(timedelta(hours=5, minutes=30))
LOCK_AFTER, LOCK_SECONDS = 5, 300
SEARCHES = {}  # user id -> recent search times (simple per-user limit)


def today():
    return datetime.now(IST).date().isoformat()


def seed_demo_land():
    """A free host forgets its files when it restarts. If PORTAL_DEMO_TOKEN is set, the demo land is
    recreated with the SAME watch link each time, so the agent's saved link keeps working."""
    token = os.environ.get("PORTAL_DEMO_TOKEN", "")
    if len(token) < 20:
        return
    db = store.conn()
    if store.land_by_token(db, token) is None:
        email = "demo-landlord@demo.example"
        user = store.user_by_email(db, email)
        if user is None:
            uid = store.create_user(db, email, "Demo Landlord", "landlord", sec.hash_password(sec.new_token() + "aA1"))
            user = store.user_by_id(db, uid)
        store.add_land(db, user, {"district": "demo-district", "taluk": "demo-taluk", "hobli": "demo-hobli",
                                  "village": "demo-village", "survey_no": "101", "surnoc": "*", "hissa": "1",
                                  "extent": "5-00", "owner_name": "Demo Owner"}, token=token)
    db.close()


def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=sec.secret_key(),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.environ.get("PORTAL_HTTPS") == "1",
        PERMANENT_SESSION_LIFETIME=timedelta(hours=8),
        MAX_CONTENT_LENGTH=16 * 1024,
    )

    # ---------- plumbing
    @app.before_request
    def load():
        g.db = store.conn()
        uid = session.get("uid")
        g.user = store.user_by_id(g.db, uid) if uid else None
        if request.method == "POST":
            if not sec.same(request.form.get("csrf", ""), session.get("csrf", "x")):
                abort(400)

    @app.teardown_request
    def close(_exc):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    @app.after_request
    def headers(resp):
        resp.headers["Content-Security-Policy"] = (
            "default-src 'self'; style-src 'self' https://fonts.googleapis.com; "
            "font-src https://fonts.gstatic.com; img-src 'self' data:; frame-ancestors 'none'; form-action 'self'")
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["Referrer-Policy"] = "same-origin"
        resp.headers["Cache-Control"] = "no-store"
        return resp

    @app.context_processor
    def inject():
        if "csrf" not in session:
            session["csrf"] = sec.new_token()
        return {"csrf": session["csrf"], "user": g.user, "ts": lambda t: datetime.fromtimestamp(t, IST).strftime("%d %b %Y, %I:%M %p")}

    def need(*roles):
        def deco(fn):
            @wraps(fn)
            def wrapper(*a, **k):
                if g.user is None:
                    return redirect(url_for("login", next=request.path))
                if roles and g.user["role"] not in roles:
                    abort(403)
                return fn(*a, **k)
            return wrapper
        return deco

    def home_for(user):
        return url_for({"landlord": "dashboard", "buyer": "search", "registrar": "registrar"}[user["role"]])

    def start_session(user):
        session.clear()
        session.permanent = True
        session["uid"] = user["id"]
        session["csrf"] = sec.new_token()

    def safe_next(target):
        return target if target and target.startswith("/") and not target.startswith("//") else None

    # ---------- public pages
    @app.get("/")
    def index():
        if g.user:
            return redirect(home_for(g.user))
        return render_template("index.html", no_registrar=not store.has_registrar(g.db))

    @app.get("/healthz")
    def healthz():
        return "ok"

    @app.get("/public/<token>")
    def public_record(token):
        """Unlisted link the owner shares with the agent. Masked owner name, no login."""
        row = store.land_by_token(g.db, token)
        if row is None:
            abort(404)
        resp = app.make_response(render_template("public.html", r=store.record_view(g.db, row)))
        resp.headers["X-Robots-Tag"] = "noindex"
        return resp

    # ---------- accounts
    @app.route("/register", methods=["GET", "POST"])
    def register():
        role = request.values.get("role", "landlord")
        role = role if role in ("landlord", "buyer") else "landlord"
        if request.method == "POST":
            email = sec.clean(request.form.get("email"), 120).lower()
            name = sec.clean(request.form.get("name"), 60)
            pw, pw2 = request.form.get("password", ""), request.form.get("confirm", "")
            problem = None
            if not sec.EMAIL.match(email):
                problem = "Enter a valid email address."
            elif len(name) < 2:
                problem = "Enter your name."
            elif pw != pw2:
                problem = "The two passwords do not match."
            else:
                problem = sec.password_problem(pw, email, name)
            if problem is None and store.user_by_email(g.db, email):
                problem = "That email is already registered. Try logging in."
            if problem:
                flash(problem, "error")
                return render_template("register.html", role=role, form={"email": email, "name": name}), 400
            uid = store.create_user(g.db, email, name, role, sec.hash_password(pw))
            new_user = store.user_by_id(g.db, uid)
            start_session(new_user)
            flash("Account created. Welcome.", "ok")
            return redirect(home_for(new_user))
        return render_template("register.html", role=role, form={})

    @app.route("/login", methods=["GET", "POST"])
    def login():
        role = request.values.get("role", "")
        if request.method == "POST":
            email = sec.clean(request.form.get("email"), 120).lower()
            pw = request.form.get("password", "")
            row = store.user_by_email(g.db, email)
            now = time.time()
            if row is not None and row["locked_until"] > now:
                flash("Too many wrong attempts. Try again in a few minutes.", "error")
                return render_template("login.html", role=role), 429
            if row is None:
                sec.burn_time(pw)
            elif sec.verify_password(pw, row["pw_hash"]):
                g.db.execute("UPDATE users SET failed=0, locked_until=0 WHERE id=?", (row["id"],))
                g.db.commit()
                start_session(row)
                return redirect(safe_next(request.args.get("next")) or home_for(row))
            else:
                failed = row["failed"] + 1
                lock = now + LOCK_SECONDS if failed >= LOCK_AFTER else 0
                g.db.execute("UPDATE users SET failed=?, locked_until=? WHERE id=?",
                             (0 if lock else failed, lock, row["id"]))
                g.db.commit()
            flash("Email or password is wrong.", "error")
            return render_template("login.html", role=role), 401
        return render_template("login.html", role=role)

    @app.route("/setup", methods=["GET", "POST"])
    def setup():
        """One-time page to create the first registrar. Closes itself once one exists.
        Online it needs PORTAL_SETUP_CODE; without a code it only works from this computer."""
        if store.has_registrar(g.db):
            abort(404)
        code = os.environ.get("PORTAL_SETUP_CODE", "")
        if not code and request.remote_addr not in ("127.0.0.1", "::1"):
            abort(404)
        if request.method == "POST":
            email = sec.clean(request.form.get("email"), 120).lower()
            name = sec.clean(request.form.get("name"), 60)
            pw, pw2 = request.form.get("password", ""), request.form.get("confirm", "")
            problem = None
            if code and not hmac.compare_digest(request.form.get("code", ""), code):
                problem = "Wrong setup code."
            elif not sec.EMAIL.match(email):
                problem = "Enter a valid email address."
            elif len(name) < 2:
                problem = "Enter a name."
            elif pw != pw2:
                problem = "The two passwords do not match."
            else:
                problem = sec.password_problem(pw, email, name)
            if problem is None and store.user_by_email(g.db, email):
                problem = "That email is already registered."
            if problem:
                flash(problem, "error")
                return render_template("setup.html", need_code=bool(code), form={"email": email, "name": name}), 400
            uid = store.create_user(g.db, email, name, "registrar", sec.hash_password(pw))
            start_session(store.user_by_id(g.db, uid))
            flash("Registrar account created.", "ok")
            return redirect(url_for("registrar"))
        return render_template("setup.html", need_code=bool(code), form={})

    @app.post("/logout")
    def logout():
        session.clear()
        return redirect(url_for("index"))

    # ---------- landlord
    @app.get("/dashboard")
    @need("landlord")
    def dashboard():
        rows = [store.record_view(g.db, r) | {"token": r["public_token"]} for r in store.lands_of(g.db, g.user["id"])]
        return render_template("dashboard.html", lands=rows)

    @app.route("/lands/new", methods=["GET", "POST"])
    @need("landlord")
    def land_new():
        form = {}
        if request.method == "POST":
            f = {k: sec.clean(request.form.get(k), 60) for k in
                 ("district", "taluk", "hobli", "village", "survey_no", "surnoc", "hissa", "extent", "owner_name")}
            f["surnoc"], f["hissa"] = f["surnoc"] or "*", f["hissa"] or "0"
            f["owner_name"] = f["owner_name"] or g.user["name"]
            form = f
            problem = None
            if not all(sec.PLACE.match(f[k]) for k in ("district", "taluk", "hobli", "village")):
                problem = "District, taluk, hobli and village need letters or numbers only (2 to 60 characters)."
            elif not sec.SURVEY.match(f["survey_no"]) or not sec.SURVEY.match(f["hissa"]) or not sec.SURVEY.match(f["surnoc"].replace("*", "0")):
                problem = "Survey number, surnoc and hissa can only use letters, numbers, / and -."
            elif not sec.EXTENT.match(f["extent"]):
                problem = "Extent must look like 2-10 (acres-guntas)."
            elif len(f["owner_name"]) < 2:
                problem = "Enter the owner's name."
            elif request.form.get("own") != "yes":
                problem = "Please confirm this land belongs to you or your family."
            if problem is None:
                try:
                    lid = store.add_land(g.db, g.user, f)
                    flash("Land registered.", "ok")
                    return redirect(url_for("land_detail", land_id=lid))
                except Exception as e:  # unique constraint
                    if "UNIQUE" in str(e):
                        problem = "This survey number is already registered in the demo registry."
                    else:
                        raise
            flash(problem, "error")
            return render_template("land_new.html", form=form), 400
        return render_template("land_new.html", form=form)

    def own_land(land_id):
        row = store.land(g.db, land_id)
        if row is None or row["owner_id"] != g.user["id"]:
            abort(404)
        return row

    @app.get("/lands/<int:land_id>")
    @need("landlord")
    def land_detail(land_id):
        row = own_land(land_id)
        return render_template("land_detail.html", r=store.record_view(g.db, row), land=row,
                               events=store.events(g.db, land_id), kinds=store.KINDS,
                               watch_url=url_for("public_record", token=row["public_token"], _external=True))

    @app.post("/lands/<int:land_id>/mutation")
    @need("landlord")
    def mutation_file(land_id):
        own_land(land_id)
        kind, note = request.form.get("kind"), sec.clean(request.form.get("note"), 200)
        if kind not in store.KINDS:
            abort(400)
        if store.pending_count(g.db, land_id) >= 3:
            flash("You already have 3 pending mutations on this land. Wait for the registrar.", "error")
        else:
            ref = store.file_mutation(g.db, land_id, g.user, kind, note, today())
            flash(f"Mutation {ref} filed. It stays Pending until the registrar decides.", "ok")
        return redirect(url_for("land_detail", land_id=land_id))

    # ---------- buyer (and registrar)
    @app.get("/search")
    @need("buyer", "registrar")
    def search():
        q = {k: sec.clean(request.args.get(k), 60) for k in ("district", "taluk", "hobli", "village", "survey_no", "hissa")}
        results, searched = [], any(q.values())
        if searched:
            recent = [t for t in SEARCHES.get(g.user["id"], []) if t > time.time() - 60]
            if len(recent) >= 30:
                flash("Too many searches. Wait a minute.", "error")
                return render_template("search.html", q=q, results=[], searched=False), 429
            SEARCHES[g.user["id"]] = recent + [time.time()]
            if not (q["district"] and q["survey_no"]):
                flash("Enter at least the district and the survey number.", "error")
            else:
                results = [store.record_view(g.db, r) for r in store.search(g.db, q)]
        return render_template("search.html", q=q, results=results, searched=searched)

    @app.get("/record/<int:land_id>")
    @need("buyer", "registrar")
    def record(land_id):
        row = store.land(g.db, land_id)
        if row is None:
            abort(404)
        return render_template("record.html", r=store.record_view(g.db, row))

    # ---------- registrar
    @app.get("/registrar")
    @need("registrar")
    def registrar():
        return render_template("registrar.html", queue=store.pending_queue(g.db))

    @app.get("/registrar/lands/<int:land_id>")
    @need("registrar")
    def registrar_land(land_id):
        row = store.land(g.db, land_id)
        if row is None:
            abort(404)
        return render_template("registrar_land.html", r=store.record_view(g.db, row), land=row,
                               events=store.events(g.db, land_id))

    @app.post("/mutations/<int:mutation_id>/decide")
    @need("registrar")
    def mutation_decide(mutation_id):
        decision = request.form.get("decision")
        if decision not in ("approve", "reject"):
            abort(400)
        m = store.decide(g.db, mutation_id, g.user, decision, sec.clean(request.form.get("note"), 200), today())
        if m is None:
            abort(404)
        flash(f"{m['ref']} {'approved' if decision == 'approve' else 'rejected'}.", "ok")
        return redirect(request.form.get("back") if safe_next(request.form.get("back")) else url_for("registrar"))

    @app.post("/registrar/lands/<int:land_id>/extent")
    @need("registrar")
    def set_extent(land_id):
        extent = sec.clean(request.form.get("extent"), 10)
        if store.land(g.db, land_id) is None:
            abort(404)
        if not sec.EXTENT.match(extent):
            flash("Extent must look like 2-10.", "error")
        else:
            store.set_extent(g.db, land_id, g.user, extent)
            flash("Extent updated.", "ok")
        return redirect(url_for("registrar_land", land_id=land_id))

    @app.post("/registrar/lands/<int:land_id>/owner")
    @need("registrar")
    def set_owner(land_id):
        name = sec.clean(request.form.get("owner_name"), 60)
        if store.land(g.db, land_id) is None:
            abort(404)
        if len(name) < 2:
            flash("Enter the new owner's name.", "error")
        else:
            store.set_owner(g.db, land_id, g.user, name)
            flash("Ownership transfer recorded.", "ok")
        return redirect(url_for("registrar_land", land_id=land_id))

    @app.errorhandler(403)
    def forbidden(_e):
        return render_template("error.html", code=403, text="You do not have access to this page."), 403

    @app.errorhandler(404)
    def missing(_e):
        return render_template("error.html", code=404, text="We could not find that page."), 404

    @app.errorhandler(400)
    def bad(_e):
        return render_template("error.html", code=400, text="That request could not be processed. Go back and try again."), 400

    # first start on a server: create the registrar from settings if none exists
    email, pw = os.environ.get("PORTAL_REGISTRAR_EMAIL"), os.environ.get("PORTAL_REGISTRAR_PASSWORD")
    if email and pw:
        db = store.conn()
        if not store.has_registrar(db):
            store.create_user(db, email.lower(), "Demo Registrar", "registrar", sec.hash_password(pw))
        db.close()
    seed_demo_land()
    return app


app = None


def get_app():
    """Server entry: gunicorn 'src.portal.app:get_app()'."""
    global app
    if app is None:
        app = create_app()
    return app
