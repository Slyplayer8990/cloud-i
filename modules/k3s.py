import libvirt
import sqlite3
import shutil
import time
import uuid
import os
import xml.etree.ElementTree as ET
cnx = sqlite3.connect('/var/lib/cloudy/cloudy.db')
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
  metadata = """local-thosname: """ + master_name + """
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
  num = str(uuid.uuid4())
  root = ET.Element("domain", type="qemu")
  name1 = ET.SubElement(root, "name")
  name1.text = master_name
  uuid1 = ET.SubElement(root, "uuid")
  uuid1.text = num
  memory1 = ET.SubElement(root, "memory", unit="MB")
  memory1.text = "512"
  vcpu1 = ET.SubElement(root, "vcpu")
  vcpu1.text = "1"
  os1 = ET.SubElement(root, "os")
  type1 = ET.SubElement(os1, "type")
  type1.text = "hvm"
  boot1 = ET.SubElement(os1, "boot", dev="hd")
  smbios1 = ET.SubElement(os1, "smbios", mode="sysinfo")
  sysinfo1 = ET.SubElement(root, "sysinfo", type="smbios")
  bios1 = ET.SubElement(sysinfo1, "bios")
  entry1 = ET.SubElement(bios1, "entry", name="vendor")
  entry1.text = "Cloudy"
  system1 = ET.SubElement(sysinfo1, "system")
  entry2 = ET.SubElement(system1, "entry", name="manufacturer")
  entry2.text = "Cloudy"
  entry3 = ET.SubElement(system1, "entry", name="product")
  entry3.text = "Cloudy Virtual Machine Delivery"
  entry4 = ET.SubElement(system1, "entry", name="version")
  entry4.text = "1.0.0"
  entry5 = ET.SubElement(system1, "entry", name="serial")
  entry5.text = "ds=nocloud-net;s=http://http://192.168.122.1:8080/cloudy/api/k3s/seeds/" + name + "/master/"
  clock1 = ET.SubElement(sysinfo1, "clock", offset="utc")
  on_poweroff1 = ET.SubElement(root, "on_poweroff")
  on_poweroff1.text = "destroy"
  on_reboot1 = ET.SubElement(root, "on_reboot")
  on_reboot1.text = "restart"
  on_crash1 = ET.SubElement(root, "on_crash")
  on_crash1.text = "restart"
  devices1 = ET.SubElement(root, "devices")
  emulator1 = ET.SubElement(devices1, "emulator")
  emulator1.text = "/usr/bin/kvm-spice"
  disk1 = ET.SubElement(devices1, "disk", type="file", device="disk")
  driver1 = ET.SubElement(disk1, "driver", name="qemu", type="raw")
  source1 = ET.SubElement(disk1, "source", file=masterlocation)
  target1 = ET.SubElement(disk1, "target", dev="vda", bus="virtio")
  interface1 = ET.SubElement(devices1, "interface", type="network")
  source2 = ET.SubElement(interface1, "source", network="default")
  model1 = ET.SubElement(interface1, "model", type="virtio")
  address1 = ET.SubElement(interface1, "address", type="pci", domain="0x0000", bus="0x00", slot="0x03", function="0x0")
  serial1 = ET.SubElement(devices1, "serial", type="pty")
  target2 = ET.SubElement(serial1, "target", port="0")
  console1 = ET.SubElement(devices1, "console", type="pty")
  target3 = ET.SubElement(console1, "target", type="serial", port="0")
  ET.ElementTree(root).write("/etc/libvirt/qemu/" + master_name + ".xml")
  masterxml = open("/etc/libvirt/qemu/" + master_name + ".xml", "r")
  dom = cnx2.defineXML(masterxml)
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
    root = ET.Element("domain", type="qemu")
    name1 = ET.SubElement(root, "name")
    name1.text = node_name
    uuid1 = ET.SubElement(root, "uuid")
    uuid1.text = num
    memory1 = ET.SubElement(root, "memory", unit="MB")
    memory1.text = "512"
    vcpu1 = ET.SubElement(root, "vcpu")
    vcpu1.text = "1"
    os1 = ET.SubElement(root, "os")
    type1 = ET.SubElement(os1, "type")
    type1.text = "hvm"
    boot1 = ET.SubElement(os1, "boot", dev="hd")
    smbios1 = ET.SubElement(os1, "smbios", mode="sysinfo")
    sysinfo1 = ET.SubElement(root, "sysinfo", type="smbios")
    bios1 = ET.SubElement(sysinfo1, "bios")
    entry1 = ET.SubElement(bios1, "entry", name="vendor")
    entry1.text = "Cloudy"
    system1 = ET.SubElement(sysinfo1, "system")
    entry2 = ET.SubElement(system1, "entry", name="manufacturer")
    entry2.text = "Cloudy"
    entry3 = ET.SubElement(system1, "entry", name="product")
    entry3.text = "Cloudy Virtual Machine Delivery"
    entry4 = ET.SubElement(system1, "entry", name="version")
    entry4.text = "1.0.0"
    entry5 = ET.SubElement(system1, "entry", name="serial")
    entry5.text = "ds=nocloud-net;s=http://
    entry6 = ET.SubElement(system1, "entry", name="uuid")
    entry6.text = num
    nodexml = """<domain type='qemu'>
      <name>""" + node_name + """</name>
      <uuid>""" + num + """ </uuid>
      <memory unit="MB">512</memory>
      <vcpu>1</vcpu>
      <os>
        <type>hvm</type>
        <boot dev='hd'/>
        <smbios mode='sysinfo'/>
      </os>
      <sysinfo type='smbios'>
      <bios>
        <entry name='vendor'>Cloudy</entry>
      </bios>
      <system>
        <entry name='manufacturer'>Cloudy</entry>
        <entry name='product'>Cloudy Virtual Machine Delivery</entry>
        <entry name='version'>1.0.0</entry>
        <entry name='serial'>ds=nocloud-net;s=http://192.168.122.1:8080/cloudy/api/k3s/seeds/""" + name + "/node/" + node_name + """</entry>
      </system>
      <clock offset='utc'/>
      <on_poweroff>destroy</on_poweroff>
      <on_reboot>restart</on_reboot>
      <on_crash>restart</on_crash>
      <devices>
        <emulator>/usr/bin/qemu-system-x86_64</emulator>
        <disk type='file' device='disk'>
          <source file='""" + nodelocation + """'/>
          <driver name='qemu' type='raw'/>
          <target dev='hda'/>
        </disk>
        <interface type='bridge'>
          <source bridge='virbr0'/>
          <model type='virtio'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
        </interface>
        <serial type="pty">
          <target type="isa-serial" port="0">
            <model name="isa-serial"/>
          </target>
        </serial>
      </devices>
    </domain>"""
    dom = cnx2.defineXML(nodexml)
    try:
      dom.create()
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

