from django.db import models


class Disaster(models.Model):
    class Meta:
        db_table = "disaster"
    disaster_request_no = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=50)
    benefit_begin_date = models.DateField(null=False)
    benefit_end_date = models.DateField(null=False)
    state_or_territory = models.CharField(max_length=2)
    is_residency_required = models.BooleanField()
    uses_DSED = models.BooleanField()

    def __str__(self):
        return '{}: {}'.format(self.disaster_request_no, self.title)
