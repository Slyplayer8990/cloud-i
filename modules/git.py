import os
import psycopg2
conn = psycopg2.connect(database="cloudy",
                        host="127.0.0.1",
                        user="cloudy",
                        password="cloudy123",
                        port="5432",
                        buffered=true)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS repository (
    name    VARCHAR(16),
    creator VARCHAR(16),
    private BOOLEAN     
)")
def createrepo(name):
    os.chdir("/home/git")
    os.system("mkdir" + name + ".git")
    os.chdir(name + ".git")
    os.system("git init --bare")
def delrepo(name):
    os.chdir("/home/git")
    os.system("rm -rf " + name + ".git")