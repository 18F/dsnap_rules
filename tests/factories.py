import factory

from dsnap_rules import models


class DisasterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'dsnap_rules.Disaster'

    disaster_request_no = factory.Faker('pystr')
    title = factory.Faker('pystr')
    state = factory.Iterator(models.State.objects.all())
    benefit_begin_date = factory.Faker('date')
    benefit_end_date = factory.Faker('date')
    residency_required = factory.Faker('boolean')
    uses_DSED = factory.Faker('boolean')
    allows_food_loss_alone = factory.Faker('boolean')


class ApplicationPeriodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'dsnap_rules.ApplicationPeriod'

    begin_date = factory.Faker('date')
    end_date = factory.Faker('date')
    registration_begin_date = factory.Faker('date')
    registration_end_date = factory.Faker('date')
