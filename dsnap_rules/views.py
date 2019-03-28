import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .dsnap_application import DSNAPApplication
from .dsnap_rules import (AdverseEffectRule, AuthorizedRule,
                          FoodPurchaseRule,
                          IncomeAndResourceRule, DisasterAreaResidencyRule,
                          SNAPSupplementalBenefitsRule)
from .models import Disaster
from .rules import And
from .serializers import DisasterSerializer
from .validate import validate

logger = logging.getLogger(__name__)


@api_view(['GET', 'POST'])
@csrf_exempt
def index(request):
    if request.method == 'GET':
        disasters = Disaster.objects.order_by('disaster_request_no')
        context = {"disaster_list": disasters}
        return render(request, 'dsnap_rules/demo_form.html', context)

    data = request.data

    try:
        valid, messages = validate(data)
        if not valid:
            response = jsonify(message=messages)
            response.status_code = 400
            return response
    except Exception:
        logger.exception("Failed validation")

    try:
        disaster = Disaster.objects.get(
            disaster_request_no=data["disaster_request_no"])
    except Disaster.DoesNotExist:
        response = jsonify(message="Disaster {} not found".format(
            data["disaster_request_no"]))
        response.status_code = 404
        return response
    except Exception:
        logger.exception("Failed to retrieve a disaster")

    try:
        application = DSNAPApplication(data)
        result = And(
            AuthorizedRule(),
            AdverseEffectRule(),
            FoodPurchaseRule(),
            DisasterAreaResidencyRule(),
            SNAPSupplementalBenefitsRule(),
            IncomeAndResourceRule()
        ).execute(application, disaster)

        return jsonify(
            eligible=result.successful,
            findings=result.findings,
            metrics=result.metrics,
            state=disaster.state.abbreviation
        )
    except Exception:
        logger.exception("Failed to execute rules")


@api_view(['GET'])
@csrf_exempt
def disaster_list(request):
    """
    Returns active disasters, i.e., disasters that have one or more application
    periods which have registration periods that span the current date
    """
    today = timezone.localdate()
    disasters = Disaster.objects.filter(
        application_periods__registration_begin_date__lte=today).filter(
        application_periods__registration_end_date__gte=today).distinct()
    serializer = DisasterSerializer(disasters, many=True)
    return Response(serializer.data)


def jsonify(**kwargs):
    return JsonResponse(kwargs, json_dumps_params={"indent": 2})
