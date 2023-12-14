# ☁ Cloud-E, Run cloud infrastructure on premises ☁
With this software, you can easily run cloud infrastructure in your company, in your home network and anywhere you want!
You can create and terminate VMs, kubernetes clusters; you can manage your git projects; you can manage your user accounts...
(We will provide updated images as frequent as possible.)
And you can manage these things however you want(REST API, WEB interface, terminal CLI)
<br/><a href="https://hub.docker.com/r/slyplayer8990/cloud-v"><img src="https://img.shields.io/badge/Docker-Repository-03fcdf"</img></a> <a><img src="https://github.com/slyplayer8990/cloud-v/actions/workflows/docker-image.yml/badge.svg"></img></a>
# 📦 How to setup? 📦
There are many ways to setup cloud-v. Like:
1-Using our debian distro.
2-Using our container.
3-Pulling the source code and running it
## 1-Using our debian distro
You can install our distro from releases page that you can access from badges above. Then you will only setup debian like you would do in normal. Your cloud-v will prepare itself on the background while you drink your coffee.
## 2-Using our container
It is the easiest way to run cloud-v you just need to run: <br/>
a)safe method <br/>
```docker run --publish=47470:47470 --publish=47471:47471 --dev=/dev/kvm slyplayer8990/cloud-v``` <br/>
b)unsafe method <br/>
```docker run --publish=47470:47470 --publish=47471:47471 --privileged slyplayer8990/cloud-v``` <br/>
## 3- Pulling the source code and running it
It is so easy too. Just pull the repository and run the below command: <br/>
```under development```
