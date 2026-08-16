import os               

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    rows = db.execute(
        """
        SELECT symbol, SUM(shares) AS shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING shares > 0
        """,
        session["user_id"]
    )

    portfolio = []
    total_stock_value = 0

    for row in rows:
        stock = lookup(row["symbol"])
        total = stock["price"] * row["shares"]
        total_stock_value += total

        portfolio.append({
            "symbol": row["symbol"],
            "shares": row["shares"],
            "price": stock["price"],
            "total": total
        })

    cash = db.execute(
        "SELECT cash FROM users WHERE id = ?",
        session["user_id"]
    )[0]["cash"]

    grand_total = total_stock_value + cash

    return render_template(
        "index.html",
        portfolio=portfolio,
        cash=cash,
        grand_total=grand_total
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("missing symbol")

        stock = lookup(symbol)
        if stock is None:
            return apology("invalid symbol")

        try:
            shares = int(shares)
            if shares <= 0:
                raise ValueError
        except:
            return apology("shares must be a positive integer")

        price = stock["price"]
        total_cost = price * shares

        cash = db.execute(
            "SELECT cash FROM users WHERE id = ?",
            session["user_id"]
        )[0]["cash"]

        if total_cost > cash:
            return apology("can't afford")

        # Update cash
        db.execute(
            "UPDATE users SET cash = cash - ? WHERE id = ?",
            total_cost, session["user_id"]
        )

        # Record transaction
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, type) VALUES (?, ?, ?, ?, 'BUY')",
            session["user_id"], stock["symbol"], shares, price
        )

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    rows = db.execute(
        "SELECT * FROM transactions WHERE user_id = ? ORDER BY timestamp DESC",
        session["user_id"]
    )

    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":

        symbol = request.form.get("symbol")
        if not symbol:
            return apology("missing symbol")

        stock = lookup(symbol)
        if stock is None:
            return apology("invalid symbol")

        return render_template("quoted.html", stock=stock)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username")

        if not password or not confirmation:
            return apology("must provide password")

        if password != confirmation:
            return apology("passwords do not match")

        hash_pw = generate_password_hash(password)

        try:
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username, hash_pw
            )
        except ValueError:
            return apology("username already exists")

        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    stocks = db.execute(
        """
        SELECT symbol, SUM(shares) AS shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING shares > 0
        """,
        session["user_id"]
    )

    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("missing symbol")

        try:
            shares = int(shares)
            if shares <= 0:
                raise ValueError
        except:
            return apology("shares must be positive integer")

        owned = next((s for s in stocks if s["symbol"] == symbol), None)

        if owned is None or shares > owned["shares"]:
            return apology("not enough shares")

        stock = lookup(symbol)
        price = stock["price"]
        total_gain = price * shares

        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?",
            total_gain, session["user_id"]
        )

        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, type) VALUES (?, ?, ?, ?, 'SELL')",
            session["user_id"], symbol, -shares, price
        )

        return redirect("/")

    else:
        return render_template("sell.html", stocks=stocks)
