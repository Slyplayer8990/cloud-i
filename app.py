from flask import Flask, request, jsonify, send_file
import os
import json
import sys 
sys.path.insert(0, "./modules")
import schedule
import time
import machines
import psycopg2

conn = psycopg2.connect(database="cloudy",
                        host="127.0.0.1",
                        user="cloudy",
                        password="cloudy123",
                        port="5432")

app = Flask(__name__)
@app.route("/cloudy/api/login",methods=["POST"])
def login():
    try:
        username=request.json["username"]
        password=request.json["password"]
        cursor = conndb.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    except:
        return {"status": "failed"}

@app.route("/cloudy/api/machines/create",methods=["POST"])
def creation():
    requiredjson = set(["instance_name", "image", "username", "storage", "memory", "vcpu", "access_key"])
    setrequest = set(request.json)
        cursor.execute('SELECT * FROM machines WHERE instance_name=?', (instance_name,))
        result = cursor.fetchone()
        if not result is None:
            return {"alert": "Instance already exists!"}, 403
        else:
            machines.create(git push)
            return {"result": "Successfully created the machine,now you can access it!"}
    else:
        return {"alert": "Missing information, could not process it!"}, 422
    cursor.close()
@app.route("/cloudy/api/machines/seeds/<instance_name>/user-data",methods=["GET"])
def seeds_userdata(instance_name):
    print("User-data agent is:" + request.headers["User-Agent"])
    cursor = conndb.cursor()
    cursor.execute('SELECT * FROM seeds WHERE instance_name=?', (instance_name,))
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
    cursor.execute('SELECT * FROM seeds WHERE instance_name=?', (instance_name,))
    result = cursor.fetchone()
    if not result is None:
        meta_data = result[2]
        return meta_data
    else:
        return {"alert": "You aren't a cloudy instance"}, 403
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
        return {"alert": "Missing object, couldn't process it!"}, 422
@app.route("/cloudy/api/k3c/seeds/<cluster_name>/maestro/meta-data", methods=["GET"])
def k3c_metadata():
    print(request.headers["User-Agent"])
    return {"hello"}
@app.route("/cloudy/api/k3c/seeds/<cluster_name>/maestro/user-data", methods=["GET"])
def k3c_userdata(cluster_name):
    print(request.headers["User-Agent"])
    cursor = conndb.cursor()
    cursor.execute('UPDATE k3c_clusters SET cluster_ip=? WHERE cluster_name=?', (request.remote_addr, cluster_name))
    return {"hello"}
@app.route("/cloudy/api/k3c/seeds/<cluster_name>/maestro/vendor-data", methods=["GET"])
def k3c_vendordata():
    print(request.headers["User-Agent"])
    return """vendor_data:
    enabled: False"""
@app.route("/cloudy/api/s2/<user>/<bucket>/", methods=["GET", "POST"])
def file_operations(user,bucket):
    if request.method == "POST":
        user = request.headers["Cookies"]



app.run(host="0.0.0.0", port="47470")
