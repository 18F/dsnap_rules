from flask import Flask, render_template, request, jsonify
from jsonschema.exceptions import ValidationError

from new_rules.config import get_config
from new_rules.validate import validate
from new_rules.dsnap.dsnap_rules import (
    AdverseEffectRule,
    AuthorizedRule,
    ConflictingUSDAProgramRule,
    FoodPurchaseRule,
    IncomeAndResourceRule,
    ResidencyRule,
)
from new_rules.rules import And

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/', methods=['GET', 'POST'])
def run():
    if request.method == 'GET':
        return render_template('form.html')

    data = request.get_json(force=True)

    try:
        validate(data)
    except ValidationError as ve:
        response = jsonify(message=ve.message)
        response.status_code = 400
        return response

    config = get_config()

    result = And(
            AuthorizedRule(),
            AdverseEffectRule(),
            FoodPurchaseRule(),
            ResidencyRule(),
            ConflictingUSDAProgramRule(),
            IncomeAndResourceRule()
    ).execute(data, config)

    return jsonify(
        eligible=result.successful,
        findings=result.findings,
        metrics=result.metrics
    )
