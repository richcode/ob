from flask import Flask, jsonify
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


@app.route('/procurements', methods=['GET'])
def procurements():
    procurements = Procurements.query.filter_by(agency='Accounting And Corporate Regulatory Authority')
    for row in procurements:
        print(row.tender_no)
    return 'test'

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