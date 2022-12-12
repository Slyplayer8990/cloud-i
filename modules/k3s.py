import libvirt
import mysql.connector
import shutil
cnx = mysql.connector.connect(
     host="localhost",
     user="cloudy",
     password="cloudy123",
     database="cloudy",
     auth_plugin="mysql_native_password"
)
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
  metadata = """local-hosname: """ + master_name + """
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
  image = "/var/lib/cloudy/images/ubuntu-cloudy.raw"
  masterlocation = "/var/lib/cloudy/machines" + master_name + ".raw"
  shutil.copyfile(image, masterlocation)
  masterxml = """<domain type='qemu'>
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
          <source file='""" + machinelocation + """'/>
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
  dom = conn.defineXML(xmlconfig)
  try:
    dom.create()     
  except:
    print("We are ashamed to say but...")


