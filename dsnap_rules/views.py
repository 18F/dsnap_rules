from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from jsonschema.exceptions import ValidationError

from .decorators import json_request
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
from .models import Disaster


@csrf_exempt
@json_request
def index(request):
    if request.method == 'GET':
        disasters = Disaster.objects.order_by('disaster_request_no')
        context = {"disaster_list": disasters}
        return render(request, 'dsnap_rules/demo_form.html', context)

    data = request.json

    try:
        validate(data)
    except ValidationError as ve:
        response = jsonify(message=ve.message)
        response.status_code = 400
        return response

    try:
        disaster = Disaster.objects.get(
            disaster_request_no=data["disaster_request_no"])
    except Disaster.DoesNotExist:
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


def jsonify(**kwargs):
    return JsonResponse(kwargs, json_dumps_params={"indent": 2})
