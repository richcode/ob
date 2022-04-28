from app import db

class Procurements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tender_no = db.Column(db.String(255))
    tender_description = db.Column(db.Text())
    agency = db.Column(db.String(255))
    award_date = db.Column(db.DateTime())
    tender_detail_status = db.Column(db.String(100))
    supplier_name = db.Column(db.String(255))
    awarded_amt = db.Column(db.Float())