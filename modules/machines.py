
import os
import shutil
import sys
import uuid
import xml.etree.ElementTree as ET
from imp import source_from_cache
from venv import create
import libvirt
import psycopg2

conn = psycopg2.connect(database="cloudy",
                        host="127.0.0.1",
                        user="cloudy",
                        password="cloudy123",
                        port="5432")


def initdb():
    """ """
    cursor = cnx.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS seeds (name TEXT, userdata TEXT, metadata TEXT)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS machines (name TEXT, uuid TEXT, memory TEXT, vcpu TEXT, storage TEXT, image TEXT, user TEXT, ssh_key TEXT, status TEXT)"
    )
    cursor.close()
    cnx.commit()


initdb()
conn = libvirt.open("qemu:///system")
userdata = None
metadata = None
seedlocation = None


def createseed(name, user, ssh_key):
    """

    :param name:
    :param user:
    :param ssh_key:

    """
    cursor = cnx.cursor()
    userdata = ("""#cloud-config
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
""")
    metadata = ("""local-hosname: """ + name + """
network-interfaces: |
     auto eth0
     iface eth0 inet dhcp
     """)
    cursor.execute("INSERT INTO seeds VALUES (?,?,?);",
                   (name, userdata, metadata))
    cursor.close()
    cnx.commit()


def create(instance_name, image_name, username, storage, memory, vcpu,
           user_providen_ssh_key):
    """

    :param instance_name:
    :param image_name:
    :param username:
    :param storage:
    :param memory:
    :param vcpu:
    :param user_providen_ssh_key:

    """
    uuidnum = uuid.uuid4()
    num = str(uuidnum)
    image = image_name + "-cloudy"
    source = "/var/lib/cloudy/images/" + image + ".qcow2"
    machinelocation = "/var/lib/cloudy/machines/" + instance_name + ".qcow2"
    shutil.copyfile(source, machinelocation)
    storage1 = int(storage)
    os.system("qemu-img resize " + machinelocation + " " + storage1 + "G")
    createseed(instance_name, username, user_providen_ssh_key, cloudHost)

    root = ET.Element("domain")
    root.set("type", "kvm")
    name = ET.SubElement(root, "name")
    name.text = instance_name
    memory = ET.SubElement(root, "memory")
    memory.text = memory
    vcpu = ET.SubElement(root, "vcpu")
    vcpu.text = vcpu
    os = ET.SubElement(root, "os")
    type = ET.SubElement(os, "type")
    type.text = "hvm"
    boot = ET.SubElement(os, "boot")
    boot.set("dev", "hd")
    smbios = ET.SubElement(os, "smbios")
    smbios.set
    sysinfo = ET.SubElement(root, "sysinfo")
    sysinfo.set("type", "smbios")
    bios = ET.SubElement(root, "bios")
    biosentry = ET.SubElement(bios, "entry")
    biosentry.set("name", "vendor")
    biosentry.text = "Cloudy"
    system = ET.SubElement(root, "system")
    systementry = ET.SubElement(system, "entry")
    systementry.set("name", "manufacturer")
    systementry.text = "Cloudy"
    systementry2 = ET.SubElement(system, "entry")
    systementry2.set("name", "product")
    systementry2.text = "Cloudy Virtual Machine"
    systementry3 = ET.SubElement(system, "entry")
    systementry3.set("name", "version")
    systementry3.text = "1.0"
    systementry4 = ET.SubElement(system, "entry")
    systementry4.set("name", "serial")
    systementry4.text = (
        "ds=nocloud-net;s=http://" + cloudHost + "/cloudy/api/cmd/seeds/" +
        instance_name)
    clock = ET.SubElement(root, "clock")
    clock.set("offset", "utc")
    on_poweroff = ET.SubElement(root, "on_poweroff")
    on_poweroff.text = "destroy"
    on_reboot = ET.SubElement(root, "on_reboot")
    on_reboot.text = "restart"
    on_crash = ET.SubElement(root, "on_crash")
    on_crash.text = "destroy"
    devices = ET.SubElement(root, "devices")
    emulator = ET.SubElement(devices, "emulator")
    emulator.text = "/usr/bin/qemu-system-x86_64"
    disk = ET.SubElement(devices, "disk")
    disk.set("type", "file")
    disk.set("device", "disk")
    disksource = ET.SubElement(disk, "source")
    disksource.set("file",
                   "/var/lib/cloudy/machines/" + instance_name + ".qcow2")
    diskdriver = ET.SubElement(disk, "driver")
    diskdriver.set("name", "qemu")
    diskdriver.set("type", "qcow2")
    target = ET.SubElement(disk, "target")
    target.set("dev", "hda")
    interface = ET.SubElement(devices, "interface")
    interface.set("type", "bridge")
    interface_source = ET.SubElement(interface, "source")
    interface_source.set("bridge", "virbr0")
    interface_model = ET.SubElement(interface, "model")
    interface_model.set("type", "virtio")
    interface_address = ET.SubElement(interface, "address")
    interface_address.set("type", "pci")
    interface_address.set("domain", "0x0000")
    interface_address.set("bus", "0x00")
    interface_address.set("slot", "0x03")
    interface_address.set("function", "0x0")
    serial = ET.SubElement(devices, "serial")
    serial.set("type", "pty")
    serial_target = ET.SubElement(serial, "target")
    serial_target.set("type", "isa-serial")
    serial_target.set("port", "0")
    serial_target_model = ET.SubElement(serial_target, "model")
    serial_target_model.set("name", "isa-serial")
    ET.ElementTree(root).write("/etc/libvirt/qemu/" + instance_name + ".xml")
    xmlconfig = open("/etc/libvirt/qemu/" + instance_name + ".xml").read()
    domain = conn.defineXML(xmlconfig)
    try:
        domain.create()
    except:
        raise Exception("We are ashamed to say but...")
    cursor = cnx.cursor()
    cursor.execute(
        "INSERT INTO machines VALUES (?,?,?,?,?,?,?,?);",
        (
            instance_name,
            num,
            image_name,
            username,
            storage,
            memory,
            vcpu,
            user_providen_ssh_key,
        ),
    )


def terminate(instance_name):
    """

    :param instance_name:

    """
    dom = conn.lookupByName(instance_name)
    dom.destroy()
    dom.undefine(delete_storage=True)
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM seeds WHERE instance_name=?;",
                   (instance_name, ))


def stop(instance_name):
    """

    :param instance_name:

    """
    try:
        dom = conn.lookupByName(instance_name)
        dom.destroy()
    except:
        raise Exception("Something bad happened...")


def start(instance_name):
    """

    :param instance_name:

    """
    try:
        dom = conn.lookupByName(instance_name)
        dom.create()
    except:
        raise Exception("Something bad happened...")


def restart(instance_name):
    """

    :param instance_name:

    """
    try:
        dom = conn.lookupByName(instance_name)
        dom.reset()
    except:
        raise Exception(
            "Something bad happened... But i believe you can solve it... :)")

