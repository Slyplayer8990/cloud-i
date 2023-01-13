#requirements: libvirt-clients libvirt-dev libvirt-daemon libvirt-daemon-system qemu-x86_64 genisoimage
from imp import source_from_cache
import sys
import uuid
from venv import create
import libvirt
import shutil
import os
import mysql.connector
cnx = mysql.connector.connect(user="cloudy", password="cloudy123", host="localhost", database="cloudy", buffered=True) 
def initdb():
     cursor = cnx.cursor()
     cursor.execute('CREATE TABLE IF NOT EXISTS seeds (name TEXT, userdata TEXT, metadata TEXT)')
     cursor.execute('CREATE TABLE IF NOT EXISTS machines (name TEXT, uuid TEXT, memory TEXT, vcpu TEXT, storage TEXT, image TEXT, user TEXT, ssh_key TEXT, status TEXT)')
     cursor.close()
     cnx.commit()
initdb()
conn = libvirt.open("qemu:///system")
userdata = None
metadata = None
seedlocation = None
def createseed(name, user, ssh_key):
     cursor = cnx.cursor()
     userdata = """#cloud-config
groups:
  - admingroup: [root,sys]
  - cloud-users
users:
  - name: """ + user + """
    groups: users, sudo
    ssh_authorized_keys: 
    """ + "- " + ssh_key + """
    sudo: ALL=(ALL) NOPASSWD:ALL
  - name: cloudy
    system: true
"""
     metadata = """local-hosname: """ + name + """
network-interfaces: |
     auto eth0
     iface eth0 inet dhcp
     """
     cursor.execute('INSERT INTO seeds VALUES (' + '"' + name + '","' + userdata + '","' + metadata + '");')
     cursor.close()
     cnx.commit()
def create(instance_name, image_name, username, storage, memory, vcpu, user_providen_ssh_key):
     uuidnum = uuid.uuid4()
     num = str(uuidnum)
     image = image_name + "-cloudy"
     source = "/var/lib/cloudy/images/" + image + ".raw"
     machinelocation = "/var/lib/cloudy/machines/" + instance_name + ".raw"
     shutil.copyfile(source, machinelocation) 
     os.system("qemu-img resize " + machinelocation + " " + storage + "G")
     createseed(instance_name, username, user_providen_ssh_key)
     xmlconfig = """<domain type='qemu'>
     <name>""" + instance_name + """</name>
     <uuid>""" + num + """ </uuid>
     <memory unit="MB">""" + memory + """</memory>
     <vcpu>""" + vcpu + """</vcpu>
     <os>
          <type>hvm</type>
	     <boot dev='hd'/> 
          <smbios mode='sysinfo'/>
	</os>
     <sysinfo type='smbios'>
     <bios>
          <entry name='vendor'>CLOUDY</entry>
     </bios>
     <system>
          <entry name='manufacturer'>Cloudy</entry>
          <entry name='product'>Cloudy Virtual Machine Delivery</entry>
          <entry name='version'>1.0.0</entry>
          <entry name='serial'>ds=nocloud-net;s=http://192.168.122.1:8080/cloudy/api/machines/seeds/""" + instance_name + "/" + """</entry>
     </system>
     </sysinfo>
     <clock offset='utc'/>
     <on_poweroff>destroy</on_poweroff>
     <on_reboot>restart</on_reboot>
     <on_crash>restart</on_crash>
     <devices>
          <emulator>/usr/bin/qemu-system-x86_64</emulator>
          <disk type='file' device='disk'>
               <source file='""" + machinelocation + """'/>
               <driver name='qemu' type='raw'/>
               <target dev='hda'/>
          </disk>
          <interface type='bridge'>
               <source bridge='virbr0'/>
               <model type='virtio'/>
               <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
          </interface>
          <input type='mouse' bus='ps2'/>
          <graphics type='vnc' listen='127.0.0.1'/>
          <serial type="pty">
               <target type="isa-serial" port="0">
               <model name="isa-serial"/>
               </target>
          </serial>
     </devices>
     </domain>"""
     domain = conn.defineXML(xmlconfig)
     try:
          domain.create()     
     except:
          raise Exception("We are ashamed to say but...")
     cursor = cnx.cursor()
     cursor.execute('INSERT INTO machines VALUES (' + '"' + instance_name + '","' + num + '","' + memory + '","' + vcpu + '","' + storage + '","' + image + '","' + username + '","' + user_providen_ssh_key + '");')
def terminate(instance_name):
     dom = conn.lookupByName(instance_name)
     dom.destroy()
     dom.undefine(delete_storage=True)
     cursor = cnx.cursor()
     cursor.execute('DELETE FROM seeds WHERE instance_name="' + instance_name + '";')
def stop(instance_name):
     try:
          dom = conn.lookupByName(instance_name)
          dom.destroy()
     except:
          raise Exception("Something bad happened...")
def start(instance_name):
     try:
          dom = conn.lookupByName(instance_name)
          dom.create()
     except:
          raise Exception("Something bad happened...")
def restart(instance_name):
     try:
          dom = conn.lookupByName(instance_name)
          dom.reset()
     except:
          raise Exception("Something bad happened... But i believe you can solve it... :)")
#create("kali-linux-machine-test", "hvm", "kali", "20", "2048" , "2", "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDHaf/53RtN8zX9GayeXbhiw+2LfjRfZKYo1VpsCO1SuRgudaIxtxWaK06QJAz50CakkaXR1WFl52wr9jxYrfswfoS3tggLvK8fHiW06qj63T2K2VJd1nyzaTui5+ZPaMDw5suCL1QfXYQm4hkV5BqGe4456TWSuPetKAox/RH5vECXM6JAg76ASacUtu2ID8pOh07/4ci5x/RCgYIx/qajOOJzdE4OVCpgnd7dawBqf0THpAudtFQCZqzVi+ZcqsKaUBqxM0wCNm2a4LTdBfVA2RjWHv6HSONgMZZSruniNSSMhbgO5wjnb9w+nj/JO2b8uNtwc96/KWDGUhVCR8XMfKjlZF/y4/dmvX4hBsyOASq8tHYurZg4kxjhVffxQk0IkLk3EKxM580YC1D4eZCU8oX5RlnXGWLwOucipQH6eEP3WX4y+rCQ94terrgSJAmjer1qPtC6Z4pvBcSlgfl3tZyJYomVX4qEXy6XQBXv7+EBNPnb5cI6nVrbx0cibpM= sophia@sophia-HP-Laptop-15-db1xxx")
#terminate("kali-linux-machine-test")
#stop("kali-linux-machine-test")
#start("kali-linux-machine-test")
#createseed("machine", "admin","ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDHaf/53RtN8zX9GayeXbhiw+2LfjRfZKYo1VpsCO1SuRgudaIxtxWaK06QJAz50CakkaXR1WFl52wr9jxYrfswfoS3tggLvK8fHiW06qj63T2K2VJd1nyzaTui5+ZPaMDw5suCL1QfXYQm4hkV5BqGe4456TWSuPetKAox/RH5vECXM6JAg76ASacUtu2ID8pOh07/4ci5x/RCgYIx/qajOOJzdE4OVCpgnd7dawBqf0THpAudtFQCZqzVi+ZcqsKaUBqxM0wCNm2a4LTdBfVA2RjWHv6HSONgMZZSruniNSSMhbgO5wjnb9w+nj/JO2b8uNtwc96/KWDGUhVCR8XMfKjlZF/y4/dmvX4hBsyOASq8tHYurZg4kxjhVffxQk0IkLk3EKxM580YC1D4eZCU8oX5RlnXGWLwOucipQH6eEP3WX4y+rCQ94terrgSJAmjer1qPtC6Z4pvBcSlgfl3tZyJYomVX4qEXy6XQBXv7+EBNPnb5cI6nVrbx0cibpM= sophia@sophia-HP-Laptop-15-db1xxx")

