from fastapi import FastAPI
import mysql.connector
import csv
from datetime import datetime
from pydantic import BaseModel
from fastapi_pagination import Page, add_pagination, paginate


app = FastAPI(docs_url="/docs", redoc_url=None)

mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="theadmin",
  database="obback"
)

class Suppliers(BaseModel):
    supplier_name: str

@app.get("/")
def home():
    return {"data": "Run the Restore Procurements first"}

@app.get("/procurements")
def get_procurements(page: int,size: int, agency: str, supplier: str, contracts: str):
    mycursor = mydb.cursor()
    startat=page*size
    mycursor.execute("SELECT * FROM procurements LIMIT %s, %s", (startat,size))
    procurements = mycursor.fetchall()

    return {
        "items": procurements,
        "page": page, 
        "size": size
    }

@app.delete("/procurements")
def delete_procurements(agency: str, supplier: str, contracts: str):
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM procurements")
    mydb.commit()
    return {
        "message":"Procurements sucessfully deleted"
    }

@app.post("/procurements")
def restore_procurements():
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
        "message":"Procurements sucessfully restored"
    }
   
@app.get("/suppliers")
def get_suppliers(page: int,size: int):
    mycursor = mydb.cursor()
    startat=page*size
    mycursor.execute("SELECT DISTINCT(supplier_name) FROM procurements ORDER by supplier_name LIMIT %s, %s", (startat,size))
    suppliers = mycursor.fetchall()
    return suppliers

@app.get("/agencies")
def get_agencies(page: int,size: int):
    mycursor = mydb.cursor()
    startat=page*size
    mycursor.execute("SELECT DISTINCT(agency) FROM procurements ORDER by agency LIMIT %s, %s", (startat,size))
    agency = mycursor.fetchall()
    return agency

add_pagination(app)