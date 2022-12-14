import requests 
#def fetchversion():
def receive():
    os.chdir("/var/lib/cloudy/images")
    update = requests.GET("http://127.0.0.1:8080/updates")
    for machine in update:
        words = machine.split()
        request.get(words[0])