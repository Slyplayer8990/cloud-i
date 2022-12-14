from flask import Flask, request, jsonify, send_file
import os
import dotenv
import json
import sys 
import schedule
import mysql.connector
import machines
conndb = mysql.connector.connect(
    auth_plugin="mysql_native_password",
    host="localhost",
    user="cloudy",
    password="cloudy123",
    database="cloudy",
    buffered=True
)
sys.path.insert(0, "./modules")
app = Flask(__name__)
@app.route("/cloudy/api/machines/create",methods=["POST"])
def creation():
    if ("instance_name" in request.json) and ("image" in request.json) and ("username" in request.json) and ("storage" in request.json) and ("memory" in request.json) and ("vcpu" in request.json) and ("access_key" in request.json):
        instance_name = str(request.json["instance_name"])
        image = str(request.json["image"])
        username = str(request.json["username"])
        storage = str(request.json["storage"])
        memory = str(request.json["memory"])
        vcpu = str(request.json["vcpu"])
        access_key = str(request.json["access_key"])
        cursor = conndb.cursor()
        cursor.execute('SELECT * FROM machines WHERE instance_name="' + request.json["instance_name"] + '"')
        result = cursor.fetchone()
        if not result is None:
            return {"alert": "Instance already exists!"}, 403
        else:
            machines.create(instance_name, image, username, storage, memory, vcpu, access_key)
            return {"result": "Successfully created the machine,now you can access it!"}
    else:
        return {"alert": "Missing information, could not process it!"}, 422
    cursor.close()
@app.route("/cloudy/api/machines/seeds/<instance_name>/user-data",methods=["GET"])
def seeds_userdata(instance_name):
    print("User-data agent is:" + request.headers["User-Agent"])
    cursor = conndb.cursor()
    cursor.execute('SELECT * FROM seeds WHERE instance_name="' + instance_name + '"')
    result = cursor.fetchone()
    if not result is None:
        user_data = result[1]
        return user_data
    else:
        return {"alert": "You aren't a cloudy instance"}, 403
    cursor.close()
@app.route("/cloudy/api/machines/seeds/<instance_name>/meta-data",methods=["GET"])
def seeds_metadata(instance_name):
    print("User-data agent is:" + request.headers["User-Agent"])
    conndb.reconnect()
    cursor = conndb.cursor()
    cursor.execute('SELECT * FROM seeds WHERE instance_name="' + instance_name + '"')
    result = cursor.fetchone()
    if not result is None:
        meta_data = result[2]
        return meta_data
    else:
        return {"alert": "This isn't a cloudy instance"}, 403
    cursor.close()
@app.route("/cloudy/api/machines/seeds/<instance_name>/vendor-data",methods=["GET"])
def seeds_vendor_data(instance_name):
    print(instance_name)
    return """vendor_data:
    enabled: False"""
@app.route("/cloudy/api/machines/terminate",methods=["POST"])
def termination():
    if "instance_name" in request.json:
        try:
            machines.terminate(request.json["instance_name"])
        except:
            return {"alert": "This isn't a cloudy instance"}, 404
        return {"result": "Succesfully terminated machine!"}, 200
    else:
        return {"alert": "Missing object, couldn't process it!"}
@app.route("/cloudy/api/k3c/seeds/<cluster_name>/maestro/meta-data", methods=["GET"])
def k3c_metadata():
    print(request.headers["User-Agent"])
    return {hello}
app.run(host="0.0.0.0", port="47470")
