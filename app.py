from flask import Flask, request, jsonify, send_file
import os
import json
import sys 
sys.path.insert(0, "./modules")
import schedule
import time
import machines
import psycopg2
<<<<<<< HEAD
import docker
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import asyncio
client = docker.from_env()
=======
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
>>>>>>> 9bf482744c999cf3e9f3e9223b5a9f2b0855daeb
conn = psycopg2.connect(database="cloudy",
                        host="127.0.0.1",
                        user="cloudy",
                        password="cloudy123",
                        port="5432",
                        buffered=true)

app = Flask(__name__)
UPLOAD_FOLDER = '/var/cloudy/buckets'
<<<<<<< HEAD
=======

>>>>>>> 9bf482744c999cf3e9f3e9223b5a9f2b0855daeb
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
            machines.create()
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
@app.route("/cloudy/api/s2/<user>/<bucket>/", methods=["POST"])
def file_upload(user,bucket):
    if 'file' not in request.files:
        flash('No file part')
        return {"status": "Failed because of filetype=None"}
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + user + "/" + bucket + "/" + filename))
    return {"status: Complete"}
@app.route("/cloudy/api/s2/<user>/<bucket>/<file>", methods=["POST"])
def file_download(user,bucket,file):
    return send_file(app.config["UPLOAD_FOLDER"] + "/" + user + "/" + bucket + "/" + file)
<<<<<<< HEAD
@app.route("/cloudy/api/ecs/run", methods=["POST"])
def docker_run():
    if request.json["command"] is not None:
        client.containers.run(request.json["image"], request.json["command"])
        return {"status": "Completed, you can see the logs on http://hostname/cloudy/api/docker/logs/<container>"}
    if request.json["command"] is None:
        client.containers.run(requests.json["image"], detach=True)
        return {"status": "Started, you can see the logs on http://hostname/cloudy/api/docker/logs/<container>""}
=======
>>>>>>> 9bf482744c999cf3e9f3e9223b5a9f2b0855daeb
app.run(host="0.0.0.0", port="47470")

