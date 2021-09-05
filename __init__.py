from flask import Flask, Response, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy 

from datetime import datetime
import json

import config 

db = SQLAlchemy()
migrate=Migrate() 

app = Flask(__name__)
app.config.from_object(config) 

db.init_app(app)
migrate.init_app(app,db)

from . import models 

def merge_dic(x,y):
    z=x 
    z.update(y)
    return z

@app.route('/api/viewAll/',methods=["GET","OPTIONS"])
def viewAll():
    response=Response()

    if request.method=='OPTIONS':
        response.headers.add("Access-Control-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET")
    elif request.method=="GET":
        response.headers.add('Access-Control-Allow-Origin', "*")
        allTxs=models.Transaction.query.all()
        justDict={}
        for tx in allTxs:
            dictionary={'from':tx._from, 'to':tx._to, 'create_date':str(tx.create_date)}
            newDict={str(tx.id):dictionary}
            justDict=merge_dic(justDict,newDict)
        response.set_data(json.dumps(justDict, ensure_ascii=False))
    return response    
        

@app.route('/api/createTx/', methods=['POST', 'OPTIONS'])
def createTx():
    response = Response()

    if request.method=='OPTIONS':
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Aloow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST")
    elif request.method =="POST":
        response.headers.add("Access-Control-Allow-Origin", "*")
        data=request.get_json()
        data_from = data['from']
        data_to = data['to']
        tx=models.Transaction(_from=data_from, _to=data_to, create_date=datetime.now())
        db.session.add(tx)
        db.session.commit()
        response.set_data(json.dumps('True', ensure_ascii=False))
    return response

@app.route('/api/detail/txId/',methods = ['POST', 'OPTIONS'])
def detail():
    response = Response()

    if request.method=='OPTIONS':
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST")
    elif request.method=="POST":
        response.headers.add("Access-Control-Allow-Origin", "*")
        data = request.get_json()
        idx = data["id"]
        tx= models.Transaction.query.get(idx)
        justDict = {"from":tx._from, "to":tx._to, "create_date": str(tx.create_date)}
        response.set_data(json.dumps(justDict, ensure_ascii=False))
    return response


