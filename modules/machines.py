#requirements: libvirt-clients libvirt-dev libvirt-daemon libvirt-daemon-system qemu-x86_64 genisoimage
from imp import source_from_cache
import sys
import uuid
from venv import create
import libvirt
import shutil
import os
import sqlite3
cnx = sqlite3.connect('/var/lib/cloudy/cloudy.db')
import xml.etree.ElementTree as ET
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
     cursor.execute('INSERT INTO seeds VALUES (?,?,?);', (name, userdata, metadata))
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
     root = ET.Element("domain", type="qemu")
     name1 = ET.SubElement(root, "name")
     name1.text = instance_name
     uuid1 = ET.SubElement(root, "uuid")
     uuid1.text = num
     memory1 = ET.SubElement(root, "memory", unit="MB")
     memory1.text = memory
     vcpu1 = ET.SubElement(root, "vcpu")
     vcpu1.text = vcpu
     os1 = ET.SubElement(root, "os")
     type1 = ET.SubElement(os1, "type")
     type1.text = "hvm"
     boot = ET.SubElement(os1, "boot", dev="hd")
     sysinfo = ET.SubElement(root, "sysinfo", type="smbios")
     bios = ET.SubElement(sysinfo, "bios")
     entry1 = ET.SubElement(bios, "entry", name="vendor")
     entry1.text = "CLOUDY"
     system = ET.SubElement(sysinfo, "system")
     entry2 = ET.SubElement(system, "entry", name="manufacturer")
     entry2.text = "Cloudy"
     entry3 = ET.SubElement(system, "entry", name="product")
     entry3.text = "Cloudy Virtual Machine Delivery"
     entry4 = ET.SubElement(system, "entry", name="version")
     entry4.text = "1.0.0"
     entry5 = ET.SubElement(system, "entry", name="serial")
     entry5.text = "ds=nocloud-net;s=http://http://192.168.122.1:8080/cloudy/api/machines/seeds/" + instance_name + "/"
     clock = ET.SubElement(root, "clock", offset="utc")
     on_poweroff = ET.SubElement(root, "on_poweroff")
     on_poweroff.text = "destroy"
     on_reboot = ET.SubElement(root, "on_reboot")
     on_reboot.text = "restart"
     on_crash = ET.SubElement(root, "on_crash")
     on_crash.text = "restart"
     devices = ET.SubElement(root, "devices")
     emulator = ET.SubElement(devices, "emulator")
     emulator.text = "/usr/bin/qemu-system-x86_64"
     disk = ET.SubElement(devices, "disk", type="file", device="disk")
     driver = ET.SubElement(disk, "driver", name="qemu", type="raw")
     source1 = ET.SubElement(disk, "source", file=machinelocation)
     target = ET.SubElement(disk, "target", dev="vda", bus="virtio")
     interface = ET.SubElement(devices, "interface", type="network")
     source2 = ET.SubElement(interface, "source", network="default")
     model = ET.SubElement(interface, "model", type="virtio")
     graphics = ET.SubElement(devices, "graphics", type="vnc", port="-1", autoport="yes")
     video = ET.SubElement(devices, "video")
     model1 = ET.SubElement(video, "model", type="cirrus", vram="9216", heads="1")
     serial = ET.SubElement(devices, "serial", type="pty")
     console = ET.SubElement(devices, "console", type="pty")
     input1 = ET.SubElement(devices, "input", type="mouse", bus="ps2")
     input2 = ET.SubElement(devices, "input", type="keyboard", bus="ps2")
     ET.ElementTree(root).write("/etc/libvirt/qemu/" + instance_name + ".xml")
     xmlconfig = open("/etc/libvirt/qemu/" + instance_name + ".xml").read()
     domain = conn.defineXML(xmlconfig)
     try:
          domain.create()     
     except:
          raise Exception("We are ashamed to say but...")
     cursor = cnx.cursor()
     cursor.execute('INSERT INTO machines VALUES (?,?,?,?,?,?,?,?);', (instance_name, num, image_name, username, storage, memory, vcpu, user_providen_ssh_key))
def terminate(instance_name):
     dom = conn.lookupByName(instance_name)
     dom.destroy()
     dom.undefine(delete_storage=True)
     cursor = cnx.cursor()
     cursor.execute('DELETE FROM seeds WHERE instance_name=?;', (instance_name,))
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

