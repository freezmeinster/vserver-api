import os,ConfigParser
from threading import Thread


config = ConfigParser.ConfigParser()
config.readfp(open('vapi.conf')) 

V_ROOTDIR = os.popen("vserver-info APPDIR SYSINFO | grep \"Rootdir:\" | cut -d \":\" -f2").read().strip()
V_SNAPSHOT = config.get('snapshot','s_store')

vps_list = os.listdir(V_ROOTDIR)
vps_list.remove('.pkg')

class Snap(Thread):
    def __init__(self,nama):
        Thread.__init__(self)
        self.nama = nama
        
    def run(self):
        print "menjalankan %s " % self.name
        vps_dir = os.path.join(V_ROOTDIR,self.nama)
        snap_dir = os.path.join(V_SNAPSHOT,self.nama)
        os.popen("rsync -a --delete "+vps_dir+"/ "+snap_dir+"/base/")


for data in vps_list :
    os.mkdir(os.path.join(V_SNAPSHOT,data))
    snap  = Snap(data)
    snap.start()
