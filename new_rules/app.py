from flask import Flask, request, jsonify
from jsonschema.exceptions import ValidationError

from new_rules.validate import validate
from new_rules.dsnap.dsnap_rules import (
    AdverseEffectRule,
    AuthorizedRule,
    IncomeAndResourceRule,
)
from new_rules.rules import And

app = Flask(__name__)


@app.route('/', methods=['POST'])
def run():
    data = request.get_json(force=True)

    try:
        validate(data)
    except ValidationError as ve:
        response = jsonify(message=ve.message)
        response.status_code = 400
        return response

    result, findings = And(
            AuthorizedRule(),
            AdverseEffectRule(),
            IncomeAndResourceRule()
    ).execute(data)

    return jsonify(
        eligible=result,
        findings=findings
    )
