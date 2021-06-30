from flask import Blueprint, session, request, render_template, redirect, url_for, flash
from werkzeug.security import check_password_hash
from ..extentions.database import mongo


usuario = Blueprint("usuario", __name__)


@usuario.route("/")
def index():
    return redirect(url_for("usuario.login"))


@usuario.route("/main")
def main():
    if "username" in session:
        return render_template("usuarios/main.html")
    else:
        return redirect(url_for("usuario.index"))


@usuario.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("usuario.main"))
    elif request.method == "POST":
        username = request.form.get("usuario")
        password = request.form.get("senha")

        user_found = mongo.db.users.find_one({"name": username})
        if user_found:
            user_val = user_found["name"]
            passwordcheck = user_found["password"]

            if check_password_hash(passwordcheck, password):
                session["username"] = user_val
                return redirect(url_for("usuario.main"))
            else:
                flash("Senha Incorreta", "error")
                return render_template("usuarios/login.html")
        else:
            flash("Usuário não encontrado")
            return render_template("usuarios/login.html")
    return render_template("usuarios/login.html")


@usuario.route("/logout", methods=["GET"])
def logout():
    session.pop("username", None)
    flash("Logout Efetuado!")
    return redirect(url_for("usuario.login"))
