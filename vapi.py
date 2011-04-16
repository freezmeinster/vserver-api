# -*- coding: iso-8859-1 -*-
import os
import settings

class Vps:
	def init(self,**kwargs):
		nama = kwargs['nama']
		#scan Vserver-Rootdir untuk mengetahui semua Vps yang ada
		vps_list = os.listdir(settings.V_ROOTDIR)
		
		#membandingkan apakah nama VPS yang akan dibuat sudah ada atau belum 
		if nama in vps_list :
			self.on_server = True
			self.get_conf(nama)
		else :
			self.on_server = False
			
	def get_conf(self,*args):
		print args