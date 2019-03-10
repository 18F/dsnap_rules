from django.db import models


class State(models.Model):
    class Meta:
        db_table = "state"
    abbreviation = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class Disaster(models.Model):
    class Meta:
        db_table = "disaster"
    disaster_request_no = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    benefit_begin_date = models.DateField(null=False)
    benefit_end_date = models.DateField(null=False)
    state = models.ForeignKey(State, db_column="state",
                              on_delete=models.CASCADE,
                              related_name='disasters')
    residency_required = models.BooleanField()
    uses_DSED = models.BooleanField()
    allows_food_loss_alone = models.BooleanField()

    def __str__(self):
        return f'{self.disaster_request_no}: {self.title}'


class County(models.Model):
    class Meta:
        db_table = "county"
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State, db_column="state",
                              on_delete=models.CASCADE,
                              related_name='counties')

    def __str__(self):
        return f'{self.name}, {self.state}'


class ApplicationPeriod(models.Model):
    class Meta:
        db_table = "application_period"
    disaster = models.ForeignKey(Disaster, on_delete=models.CASCADE,
                                 related_name='application_periods')
    begin_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    registration_begin_date = models.DateField(null=False)
    registration_end_date = models.DateField(null=False)
    counties = models.ManyToManyField(County)

    def __str__(self):
        return ''
