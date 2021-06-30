import click
import getpass
from flask import current_app, Blueprint
from werkzeug.security import generate_password_hash
from ..extentions.database import mongo

userCommands = Blueprint("user", __name__)


@userCommands.cli.command("getUser")
@click.argument("name")
def get_user(name):
    userCollection = mongo.db.users
    user = [u for u in userCollection.find({"name": name})]
    print(user)


@userCommands.cli.command("createUser")
@click.argument("name")
def create_user(name):
    userCollection = mongo.db.users
    password = getpass.getpass()
    user = {"name": name, "password": generate_password_hash(password)}

    userExists = userCollection.find_one({"name": name})
    if userExists:
        print(f"Usuario {name} já existe")
    else:
        userCollection.insert(user)
        print(f"Usuario {name} criado com sucesso!")

 
@userCommands.cli.command("deleteUser")
@click.argument("name")
def delete_user(name):
    userCollection = mongo.db.users

    userExists = userCollection.find_one({"name": name})
    if userExists:
        question = input(f"Deseja realmente deletar o usuario {name}? (S/N) ")

        if question.upper() == "S":
            userCollection.delete_one({"name": name})
            print(f"Usuário {name} deletado com sucesso!")
        else:
            exit()
    else:
        print("Usuário não encontrado")


