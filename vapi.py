# -*- coding: iso-8859-1 -*-
import os
import settings

class Vps:
    def get(self,nama):
	#scan Vserver-Rootdir untuk mengetahui semua Vps yang ada
	vps_list = os.listdir(settings.V_ROOTDIR)
	vps_list.remove('.pkg')
	#membandingkan apakah nama VPS yang akan dibuat sudah ada atau belum 
	if nama in vps_list :
	    self.on_server = True
	    self.nama = nama
	else :
	    self.on_server = False
			
    def get_conf(self):
	vdir = os.path.join(settings.V_CONFDIR,self.nama)
	raw_mem = open(vdir+'/rlimits/rss.hard','r').read().strip()
	self.ip = open(vdir+'/interfaces/0/ip','r').read().strip()
	self.memory = str(int(raw_mem)/250)
	
    def commit_conf(self):
	ip = self.ip 
	mem = str(int(self.memory)*250)
	vdir = os.path.join(settings.V_CONFDIR,self.nama)
	ip_hendler = open(vdir+'/interfaces/0/ip','w')
	ip_hendler.write(ip)
	ip_hendler.close()
	    
	mem_hendler = open(vdir+'/rlimits/rss.hard','w')
	mem_hendler.write(mem)
	mem_hendler.close()
    
    def destroy(self):
	print "VPS dengan nama %s telah kami lenyapkan" % self.nama
	    
	
    def get_snap(self):
	pass
    
    def get_stat(self):
	pass

class VpsServer:
	
    def fetch_all(self):
	self.vps.obj = []
	vps_list = os.listdir(settings.V_ROOTDIR)
	vps_list.remove('.pkg')
	for vps in vps_list :
	    VPS = Vps()
	    VPS.get(vps)
	    VPS.get_conf()
	    self.vps_obj.append(VPS)
			

class VpsFactory:
    ip = None
    memory = None
    nama = None
    
    def save(self):
	pass
    
    

			