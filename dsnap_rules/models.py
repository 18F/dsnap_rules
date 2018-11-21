from .app import db


class Disaster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disaster_request_no = db.Column(db.String, unique=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    benefit_begin_date = db.Column(db.Date, nullable=False)
    benefit_end_date = db.Column(db.Date, nullable=False)
    state_or_territory = db.Column(db.String(2), nullable=False)
    worked_is_dsnap_eligible = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '{}: {}'.format(self.disaster_request_no, self.title)
