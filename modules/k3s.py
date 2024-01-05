import libvirt
import shutil
import time
import uuid
import os
import xml.etree.ElementTree as ET
import psycopg2
cnx = psycopg2.connect(database="cloudy",
                        host="127.0.0.1",
                        user="cloudy",
                        password="cloudy123",
                        port="5432",
                        buffered=true)
def initdb():
  cursor = cnx.cursor()
  cursor.execute('CREATE TABLE IF NOT EXISTS k3s_clusters (cluster_name TEXT, numberof_nodes INTEGER, cluster_ip TEXT, cluster_token TEXT)')
  cursor.execute('CREATE TABLE IF NOT EXISTS k3s_nodes (node_name TEXT, userdata TEXT, metadata TEXT, cluster_name TEXT)')
  cnx.commit()
  cursor.close()
  cnx.close()
initdb()
def getclusterip(name):
  cursor = cnx.cursor()
  cursor.execute('SELECT cluster_ip FROM k3s_clusters WHERE cluster_name = ?;', (name,))
  ip = cursor.fetchone()[2]
  cursor.close()
  cnx.close()
  return ip
def getclustertoken(name):
  cursor = cnx.cursor()
  cursor.execute('SELECT cluster_token FROM k3s_clusters WHERE cluster_name = ?;', (name))
  token = cursor.fetchone()[3]
  cursor.close()
  cnx.close()
  return token
try:
  cnx2 = libvirt.open("qemu:///system")
except:
  print("Couldn't connect to hypervisor!")
  raise Exception("Couldn't connect to hypervisor!")
print("SUCCESFULLY CONNECTED. :)")
def createcluster(name, numberofnodes):
  userdata = """#cloud-config
groups:
  - admingroup: [root,sys]
  - cloud-users
users:
  - name: admin
    groups: users, sudo
    sudo: ALL=(ALL) NOPASSWD:ALL
  - name: cloudy
    system: true
runcmd:
 - [ curl -sfL https://get.k3s.io | K3S_KUBECONFIG_MODE=\"644\" INSTALL_K3S_EXEC=\"server\" sh -s - ]
"""
  master_name = name + "_master"

  metadata = """local-hostname: """ + master_name + """
network-interfaces: |
     auto eth0
     iface eth0 inet dhcp
     """
  nodes = str(numberofnodes)
  cursor = cnx.cursor()
  cursor.execute('INSERT INTO k3s_clusters (cluster_name, numberof_nodes) VALUES (?, ?)', (name, nodes))
  cursor.execute('INSERT INTO k3s_nodes VALUES ("maestro",?, ?, ?);', (userdata, metadata, name))
  cnx.commit() 
  cursor.close()
  image = "/var/lib/cloudy/images/ubuntu-k3c.raw"
  masterlocation = "/var/lib/cloudy/machines" + master_name + ".raw"
  shutil.copyfile(image, masterlocation)
    uuidnum = uuid.uuid4()
    num = str(uuidnum)
    image = image_name + "-cloudy"
    source = "/var/lib/cloudy/images/" + image + ".qcow2"
    machinelocation = "/var/lib/cloudy/machines/" + master_name + ".qcow2"
    shutil.copyfile(source, masterlocation)
    os.system("qemu-img resize " + masterlocation + " 30G")
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
        "ds=nocloud-net;s=http://"+ cloudHost +"/cloudy/api/cmd/seeds/" +
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
                   "/var/lib/cloudy/machines/" + master_name + ".qcow2")
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
    ET.ElementTree(root).write("/etc/libvirt/qemu/" + master_name + ".xml")
    xmlconfig = open("/etc/libvirt/qemu/" + master_name + ".xml").read()
    domain = conn.defineXML(xmlconfig)
  try:
    dom.create()     
  except:
    print("We couldn't create the master node!")
    raise Exception("We couldn't create the master node!")
  print("Master node created!")
  time.sleep(20)

  for i in range(1, numberofnodes - 1):
    node_name = name + "_node_" + str(i)
    metadata = """local-hostname: """ + node_name + """
network-interfaces: |
      auto eth0
      iface eth0 inet dhcp
      """
    userdata = """#cloud-config
groups:
  - admingroup: [root,sys]
  - cloud-users
users:
  - name: admin
    groups: users, sudo
    sudo: ALL=(ALL) NOPASSWD:ALL
  - name: cloudy
    system: true
runcmd:
  - [ curl -sfL https://get.k3s.io | K3S_KUBECONFIG_MODE=\"644\" INSTALL_K3S_EXEC=\"agent --server http://""" + cluster_ip + """:6443\" sh -s - ]
""" 
    cursor = cnx.cursor()
    cursor.execute('INSERT INTO k3s_nodes VALUES ("' + node_name + '","' + userdata + '", "' + metadata + '", "' + name + '")')
    cnx.commit()
    cursor.close()
    image = "/var/lib/cloudy/images/ubuntu-k3c-node.raw"
    nodelocation = "/var/lib/cloudy/machines/ubuntu-k3c.raw"
    shutil.copyfile(image, nodelocation)
    os.rename(nodelocation, node_name + ".raw")


    uuidnum = uuid.uuid4()
    num = str(uuidnum)
    source = "/var/lib/cloudy/images/ubuntu-k3-node.qcow2"
    machinelocation = "/var/lib/cloudy/machines/" + node_name + ".qcow2"
    shutil.copyfile(source, nodelocation)
    os.system("qemu-img resize " + masterlocation + " 30G")
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
        "ds=nocloud-net;s=http://"+ cloudHost +"/cloudy/api/cmd/seeds/" +
        node_name)
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
    ET.ElementTree(root).write("/etc/libvirt/qemu/" + node_name + ".xml")
    xmlconfig = open("/etc/libvirt/qemu/" + node_name + ".xml").read()
    domain = conn.defineXML(xmlconfig)
    try:
      domain.create()
    except:
      print("We couldn't create the node!")
      raise Exception("We couldn't create the node!")
    print("Node created!")
    print("K3S cluster created! You can access the cluster with the following command:")

def terminate_k3s_cluster(name):
  cnx2.lookupByName(name + "_master").destroy()
  cnx2.lookupByName(name + "_master").undefine(delete_storage=True)
  cursor = cnx.cursor()
  cursor.execute('SELECT COUNT(*) FROM k3s_clusters WHERE cluster_name = "' + name + '"')
  numberofnodes = cursor.fetchone()[1]
  for i in range(1, numberofnodes):
    cnx2.lookupByName(name + "_node_" + str(i)).destroy()
    cnx2.lookupByName(name + "_node_" + str(i)).undefine(delete_storage=True)
  cursor.execute('DELETE FROM k3s_clusters WHERE cluster_name = "' + name + '"')
  cursor.execute('DELETE FROM k3s_nodes WHERE cluster_name = "' + name + '"')

