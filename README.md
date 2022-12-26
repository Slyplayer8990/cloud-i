# Cloud-E, Run cloud infrastructure on premises
With this software, you can easily run cloud infrastructure in your company, in your home network and anywhere you want!
You can create and terminate VMs, kubernetes clusters; you can manage your git projects; you can manage your user accounts...
We will provide updated VMs as frequent as possible.
And you can manage these things however you want(REST API, WEB interface, terminal CLI)
# How to install?
You need to install libvirt, git, curl, mysql-server, qemu(kvm); libvirt-dev or python3-libvirt(depending on your distribution), python3-pip packages.
After that, install required python modules by running:
```
pip install flask mysql-connector-python requests scheduler libvirt-python
```
After installing these requirements, you need to setup a mysql user with username "cloudy" and password "cloudy123" by running these commands in mysql via root user:
```
CREATE USER 'cloudy123'@'localhost' IDENTIFIED BY 'cloudy123';
```
☁Your cloud-e is ready to run!☁





