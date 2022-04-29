from flask import Flask, jsonify, request
import mysql.connector
import csv
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask("Procurements API")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:theadmin@localhost/obback'
db = SQLAlchemy(app)

mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="theadmin",
  database="obback"
)

class Procurements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tender_no = db.Column(db.String(255))
    tender_description = db.Column(db.Text())
    agency = db.Column(db.String(255))
    award_date = db.Column(db.DateTime())
    tender_detail_status = db.Column(db.String(100))
    supplier_name = db.Column(db.String(255))
    awarded_amt = db.Column(db.Float())

    def __repr__(self):
        return '<Procurements {}>'.format(self.id)


@app.get('/procurements')
def procurements():
    page = request.args.get('page', 1, type=int)
    pageSize = request.args.get('pageSize', 10, type=int)
    agency = request.args.get('agency','',type=str)
    supplier = request.args.get('supplier','',type=str)
    keyword = request.args.get('keyword','',type=str)
    procurements = Procurements.query.filter(Procurements.agency.like('%'+agency+'%')).filter(Procurements.supplier_name.like('%'+supplier+'%')).filter(Procurements.tender_description.like('%'+keyword+'%')).paginate(page, pageSize, False)
    procurementsItem = procurements.items
    data = []
    for row in procurementsItem:
        temp = {
            "tenderNo": row.tender_no,
            "tenderDescription": row.tender_description,
            "agency": row.agency,
            "awardDate": row.award_date,
            "tenderDetailStatus": row.tender_detail_status,
            "supplierName": row.supplier_name,
            "awardedAmt": row.awarded_amt,
            "yearAwarded": row.award_date
        }
        data.append(temp)
    return {
        "page": page,
        "totalPages": procurements.pages,
        "data": data
    }

@app.delete("/procurements")
def delete_procurements():
    page = request.args.get('page', 1, type=int)
    pageSize = request.args.get('pageSize', 10, type=int)
    agency = request.args.get('agency','',type=str)
    supplier = request.args.get('supplier','',type=str)
    keyword = request.args.get('keyword','',type=str)
    procurements = Procurements.query.filter(Procurements.agency.like('%'+agency+'%')).filter(Procurements.supplier_name.like('%'+supplier+'%')).filter(Procurements.tender_description.like('%'+keyword+'%')).paginate(page, pageSize, False)
    procurementsItem = procurements.items
    for row in procurementsItem:
        db.session.delete(row)
    db.session.commit()
    return {
        "message":"Procurements sucessfully deleted"
    }

@app.route('/restore', methods=['POST'])
def restore():
    mycursor = mydb.cursor()
    sql = "DELETE FROM procurements"
    mycursor.execute(sql)
    mydb.commit()

    with open('data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                award_date = datetime.strptime(row[3], '%d/%m/%Y')
                award_date = award_date.strftime('%Y-%m-%d')
                tender_no = row[0]
                tender_description = row[1]
                agency = row[2]
                tender_detail_status = row[4]
                supplier_name = row[5]
                awarded_amt = row[6]

                mycursor = mydb.cursor()
                sql = "INSERT INTO procurements (tender_no, tender_description, agency, award_date, tender_detail_status, supplier_name, awarded_amt) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = (tender_no, tender_description, agency, award_date, tender_detail_status, supplier_name, awarded_amt)
                mycursor.execute(sql, val)
                mydb.commit()
                line_count += 1
    
    return {
        "message": "Procurements sucessfully restored"
    }

@app.route('/suppliers', methods=['GET'])
def suppliers():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT DISTINCT(supplier_name) FROM procurements ORDER by supplier_name")
    agencies = mycursor.fetchall()
    row = []
    for agency in agencies:
        row.append(agency[0])
    return jsonify(row)


@app.route('/agencies', methods=['GET'])
def agencies():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT DISTINCT(agency) FROM procurements ORDER by agency")
    agencies = mycursor.fetchall()
    row = []
    for agency in agencies:
        row.append(agency[0])
    return jsonify(row)

app.run()