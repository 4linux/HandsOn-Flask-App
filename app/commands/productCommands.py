import click
from flask import current_app, Blueprint
from flask.cli import AppGroup
import json
import pandas as pd
from pymongo import collection, database

from ..extentions.database import mongo


produtos = Blueprint('produtos', __name__)
database_cli = AppGroup('mongo')
# product_collection = mongo.db.produtos


@produtos.cli.command('import')
@click.argument('csvfile')
def importcsv(csvfile):
    collection = mongo.db.produtos
    data = pd.read_csv(csvfile)
    payload = json.loads(data.to_json(orient='records'))
    collection.insert(payload)
    return collection.count()
