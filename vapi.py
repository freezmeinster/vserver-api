# -*- coding: iso-8859-1 -*-
import os
import settings

class Vps:
	def detect(self,nama):
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
		
class VpsServer:
	vps_obj = []
	
	def fetch_all(self):
		vps_list = os.listdir(settings.V_ROOTDIR)
		vps_list.remove('.pkg')
		for vps in vps_list :
			VPS = Vps()
			self.vps_obj.append(VPS.detect(vps))
			
			