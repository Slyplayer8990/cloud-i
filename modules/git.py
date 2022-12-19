import os
def createrepo(name):
    os.chdir("/home/git")
    os.system("mkdir" + name + ".git")
    os.chdir(name + ".git")
    os.system("git init --bare")
def deleterepo(name):
    os.chdir("/home/git")
    os.system("rm -rf " + name + ".git")