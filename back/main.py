from flask import Flask, jsonify, request
from flask_restx import Api, Resource, reqparse
import mysql.connector
import csv
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pandas as pd
import math


app = Flask("Procurements API")
CORS(app)
api = Api(app)
csv_org = 'data.csv'
csv_tmp = 'tmp.csv'

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

parser = reqparse.RequestParser()
parser.add_argument('page', type=str, help='Current Page')
parser.add_argument('pageSize', type=str, help='Number of item per page')
parser.add_argument('agency', type=str, help='Agency Name')
parser.add_argument('supplier', type=str, help='Supplier Name')
parser.add_argument('keyword', type=str, help='Keywords on the Contracts')

@api.route("/procurements")
class procurements(Resource):
    @api.doc(parser=parser)
    def delete(self):
        page = request.args.get('page', 1, type=int)
        pageSize = request.args.get('pageSize', 10, type=int)
        agency = request.args.get('agency','',type=str)
        supplier = request.args.get('supplier','',type=str)
        keyword = request.args.get('keyword','',type=str)

        data = []
        try:
            df = pd.read_csv(csv_tmp,dtype = {'awarded_amt': 'float64'})
        except:
            return "Invalid CSV format/data", 400

        total_pages = round(len(df) / pageSize)
        offset = (page - 1) * pageSize

        i = 0
        for index, row in df.iterrows():
            if (i==pageSize):
                break
            if (index >= offset):
                data.append({
                    'tenderNo': row['tender_no.'],
                    'tenderDescription': row['tender_description'],
                    'agency': row['agency'],
                    'awardDate': row['award_date'],
                    'tenderDetailStatus': row['tender_detail_status'],
                    'supplierName': row['supplier_name'],
                    'awardedAmt': row['awarded_amt'],
                    'yearAwarded': datetime.strptime(row['award_date'], "%Y-%m-%d").year
                })
                i = i+1

        return {
            "message":"Procurements sucessfully deleted"
        }
        
    @api.doc(parser=parser)
    def get(self):
        page = request.args.get('page', 1, type=int)
        pageSize = request.args.get('pageSize', 10, type=int)
        agency = request.args.get('agency','',type=str)
        supplier = request.args.get('supplier','',type=str)
        keyword = request.args.get('keyword','',type=str)
        offset = (page - 1) * pageSize
        data = []
        try:
            df = pd.read_csv(csv_tmp,dtype = {'awarded_amt': 'float64'})
        except:
            return "Invalid CSV format/data", 400

        if (agency):
            df.query(f'agency == "{agency}"', inplace = True)
        if (supplier):
            df.query(f'supplier_name == "{supplier}"', inplace = True)

        df_count = len(df)
        total_pages = math.ceil(float(len(df)) / pageSize)
        offset = (page - 1) * pageSize
        i = 1
        for index, row in df.iterrows():
            if (i <= pageSize):
                data.append({
                    'i': i,
                    'index': index,
                    'offset': offset,
                    'tenderNo': row['tender_no.'],
                    'tenderDescription': row['tender_description'],
                    'agency': row['agency'],
                    'awardDate': row['award_date'],
                    'tenderDetailStatus': row['tender_detail_status'],
                    'supplierName': row['supplier_name'],
                    'awardedAmt': row['awarded_amt'],
                    'yearAwarded': datetime.strptime(row['award_date'], "%Y-%m-%d").year
                })
                i = i+1

        return {
            "offset": offset,
            "page": page,
            "data": data,
            "df_count": df_count,
            "totalPages": total_pages
        }

@api.route('/restore')
class restore(Resource):
    def post(self):
        try:
            df = pd.read_csv(csv_org,dtype = {'awarded_amt': 'float64'})
        except:
            return "Invalid CSV format/data", 400

        if (df.empty) :
            return "CSV is empty", 400
        for col in df.columns:
            if (col == 'award_date'):
                try:
                        df[col] = pd.to_datetime(df[col])
                except:
                    return "Invalid award date format", 400

        df.to_csv(csv_tmp)
        return {
            "message": "Procurements sucessfully restored"
        }

@api.route('/suppliers')
class suppliers(Resource):
    def get(self):
        try:
            df = pd.read_csv(csv_tmp,dtype = {'awarded_amt': 'float64'})
        except:
            return "Invalid CSV format/data", 400

        supplier = []
        for col in df.columns:
            if (col == 'supplier_name'):
                for row in df[col]:
                    if row not in supplier:
                        supplier.append(row)

        return jsonify(supplier)


@api.route('/agencies')
class agencies(Resource):
    def get(self):
        try:
            df = pd.read_csv(csv_tmp,dtype = {'awarded_amt': 'float64'})
        except:
            return "Invalid CSV format/data", 400

        agency = []
        for col in df.columns:
            if (col == 'agency'):
                for row in df[col]:
                    if row not in agency:
                        agency.append(row)

        return jsonify(agency)
        

if __name__ == '__main__':
    app.run()