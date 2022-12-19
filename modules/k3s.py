import libvirt
import sqlite3
import shutil
import time
import uuid
def initdb():
  cnx = sqlite3.connect("cloudy.db")
  cursor = cnx.cursor()
  cursor.execute('CREATE TABLE IF NOT EXISTS k3s_clusters (cluster_name TEXT, numberof_nodes INTEGER, cluster_ip TEXT, cluster_token TEXT)')
  cursor.execute('CREATE TABLE IF NOT EXISTS k3s_nodes (node_name TEXT, userdata TEXT, metadata TEXT, cluster_name TEXT)')
  cnx.commit()
  cursor.close()
  cnx.close()
initdb()
def getclusterip(name):
  cnx = sqlite3.connect("cloudy.db")
  cursor = cnx.cursor()
  cursor.execute('SELECT cluster_ip FROM k3s_clusters WHERE cluster_name = "' + name + '"')
  ip = cursor.fetchone()[2]
  cursor.close()
  cnx.close()
  return ip
def getclustertoken(name):
  cnx = sqlite3.connect("cloudy.db")
  cursor = cnx.cursor()
  cursor.execute('SELECT cluster_token FROM k3s_clusters WHERE cluster_name = "' + name + '"')
  token = cursor.fetchone()[3]
  cursor.close()
  cnx.close()
  return token

cnx = sqlite3.connect("cloudy.db")
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
  cursor.execute('INSERT INTO k3s_clusters (cluster_name, numberof_nodes) VALUES ("' + name + '", ' + nodes + ')')
  cursor.execute('INSERT INTO k3s_nodes VALUES ("maestro", "' + userdata + '", "' + metadata + '", "' + name + '")')
  cnx.commit() 
  cursor.close()
  image = "/var/lib/cloudy/images/ubuntu-k3c.raw"
  masterlocation = "/var/lib/cloudy/machines" + master_name + ".raw"
  shutil.copyfile(image, masterlocation)
  num = str(uuid.uuid4())

  masterxml = """<domain type='qemu'>
      <name>""" + master_name + """</name>
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
        <entry name='serial'>ds=nocloud-net;s=http://192.168.122.1:8080/cloudy/api/k3s/seeds/""" + name + "/master/" + """</entry>
      </system>
      <clock offset='utc'/>
      <on_poweroff>destroy</on_poweroff>
      <on_reboot>restart</on_reboot>
      <on_crash>restart</on_crash>
      <devices>
        <emulator>/usr/bin/qemu-system-x86_64</emulator>
        <disk type='file' device='disk'>
          <source file='""" + masterlocation + """'/>
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
  dom = cnx2.defineXML(masterxml)
  try:
    dom.create()     
  except:
    print("We couldn't create the master node!")
    raise Exception("We couldn't create the master node!")
  print("Master node created!")
  time.sleep(20)

  for i in range(1, numberofnodes):
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
    nodelocation = "/var/lib/cloudy/machines/" + node_name + ".raw"
    shutil.copyfile(image, nodelocation)
    nodexml = """<domain type='qemu'>
      <name>""" + node_name + """</name>
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

