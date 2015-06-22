__author__ = 'Storagenerd'
import argparse
from pysphere import VIServer
from pysphere import VIException
from pprint import pprint
import MySQLdb as mysql
import sys

"""Variables"""
username = '*******'
password = '*******'
fqdn = '*******'
server = VIServer()
myhost = 'localhost'
myuser = '********'
mypass = '********'
mydb = 'esxprov'

"""Definitions """
def vspcon():
    try:
        server.connect(fqdn, username, password)
    except VIException:
        return None

def vspdis():
    server.disconnect()

def listvm():
    server.connect(fqdn, username, password)
    vmlist = server.get_registered_vms()
    server.disconnect()
    pprint(vmlist)

def getprop():
    server.connect(fqdn, username, password)
    vmlist = server.get_registered_vms()
    for list in vmlist:
        vm = server.get_vm_by_path(list)
        name = vm.get_property('name')
        hostname = vm.get_property('hostname')
        ip_address = vm.get_property('ip_address')
        os_type = vm.get_property('guest_full_name')
        ram = vm.get_property('memory_mb')
        cpu = vm.get_property('num_cpu')
        status = vm.get_status()
        print name, hostname, ip_address, os_type, ram, cpu, status
    server.disconnect()

def get_vmnames():
    server.connect(fqdn, username, password)
    vmlist = server.get_registered_vms()
    for list in vmlist:
        vm = server.get_vm_by_path(list)
        name = vm.get_property('name')
        print " %s" % (name)
    server.disconnect()

def proptodb():
    dbcon = mysql.connect(myhost, myuser, mypass, mydb)
    dbcur = dbcon.cursor()
    dbcur.execute("drop table vms;")
    dbcur.execute("create table vms(id int primary key auto_increment, name varchar(25), hostname varchar(50), ipaddress varchar(25), os_type varchar(50), ram varchar(25), cpu varchar(25), status varchar(25));")
    server.connect(fqdn, username, password)
    vmlist = server.get_registered_vms()
    for list in vmlist:
        vm = server.get_vm_by_path(list)
        name = vm.get_property('name')
        hostname = vm.get_property('hostname')
        ip_address = vm.get_property('ip_address')
        os_type = vm.get_property('guest_full_name')
        ram = vm.get_property('memory_mb')
        cpu = vm.get_property('num_cpu')
        status = vm.get_status()
        dbcur.execute("""insert into vms(name, hostname, ipaddress, os_type, ram, cpu, status) values (%s, %s, %s, %s, %s, %s, %s);""",(name, hostname, ip_address, os_type, ram, cpu, status))
        dbcon.commit()
    server.disconnect()

def get_result():
    dbcon = mysql.connect(myhost, myuser, mypass, mydb)
    dbcur = dbcon.cursor()
    sql = "select * from vms;"
    dbcur.execute(sql)
    result = dbcur.fetchall()
    for row in result:
        name = row[1]
        hostname = row[2]
        ip_address = row[3]
        os_type = row[4]
        ram = row[5]
        cpu = row[6]
        status = row[7]
        print "%s, %s, %s, %s, %s, %s, %s" % (name, hostname, ip_address, os_type, ram, cpu, status)

'''Run argparse'''
parser = argparse.ArgumentParser()
parser.add_argument("-v","--verbose", help="increase output verbosity",action="store_true")
parser.add_argument("-l","--vmlist", help="List all VM's",action="store_true")
parser.add_argument("-r","--result", help="List all VM's properties direct from vCenter",action="store_true")
parser.add_argument("-rh","--result_host", help="List all VM names direct from vCenter",action="store_true")
parser.add_argument("-p","--properties", help="List all VM's properties from DB",action="store_true")
parser.add_argument("-u","--updatedb", help="Update DB with latest vm config",action="store_true")
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
args = parser.parse_args()

if args.verbose:
    print("verbosity turned on")
if args.vmlist:
    listvm()
if args.properties:
    get_result()
if args.result_host:
    get_vmnames()
if args.result:
    getprop()
if args.updatedb:
    proptodb()
