import os

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from jsonschema.exceptions import ValidationError

from .validate import validate
from .dsnap_rules import (
    AdverseEffectRule,
    AuthorizedRule,
    ConflictingUSDAProgramRule,
    FoodPurchaseRule,
    IncomeAndResourceRule,
    ResidencyRule,
    SNAPSupplementalBenefitsRule,
)
from .rules import And

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    "DATABASE_URL", 'postgresql:///dsnap')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from .models import Disaster


@app.route('/', methods=['GET', 'POST'])
def run():
    if request.method == 'GET':
        return render_template('form.html', disaster_list=get_all_disasters())

    data = request.get_json(force=True)

    try:
        validate(data)
    except ValidationError as ve:
        response = jsonify(message=ve.message)
        response.status_code = 400
        return response

    try:
        disaster = get_disaster(data["disaster_request_no"])
    except NoResultFound:
        response = jsonify(message="Disaster {} not found".format(
            data["disaster_request_no"]))
        response.status_code = 404
        return response

    result = And(
            AuthorizedRule(),
            AdverseEffectRule(),
            FoodPurchaseRule(),
            ResidencyRule(),
            ConflictingUSDAProgramRule(),
            SNAPSupplementalBenefitsRule(),
            IncomeAndResourceRule()
    ).execute(data, disaster)

    return jsonify(
        eligible=result.successful,
        findings=result.findings,
        metrics=result.metrics,
        state_or_territory=disaster.state_or_territory
    )


def get_disaster(disaster_request_no):
    disaster = Disaster.query.filter_by(
        disaster_request_no=disaster_request_no).one()
    return disaster


def get_all_disasters():
    return Disaster.query.all()
