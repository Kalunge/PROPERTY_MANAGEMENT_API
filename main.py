from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from Configs.DbConfig import Devlopment
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config.from_object(Devlopment)
db = SQLAlchemy(app)
api = Api(
    app, description="A property management systmem", author="Tito & Pg", version="1.0"
)
ma = Marshmallow(app)

from Models.house import HouseModel
from Models.tenant import TenantModel
from Models.apartment import ApartmentModel
from Models.landlord import LandlordModel


@app.before_first_request
def create_all():
    db.create_all()

from Resources.landlord import *
from Resources.apartment import *
from Resources.house import *
from Resources.tenant import *


if __name__ == "__main__":
    app.run(debug=True)
