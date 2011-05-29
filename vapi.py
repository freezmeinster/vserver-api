# -*- coding: iso-8859-1 -*-
#  Vapi adalah API tidak resmi untuk Vserver .Dibuat menggunakan bahasa pemrograman Python. 
#  
#  Vapi Didistribusikan dibawah Lisensi BSD
#   
#  Untuk info lebih lanjut silahkan kunjungi http://bramandityo.com

import os,socket,shutil
from config_changer import change_sshd_config
    
V_BASEPKG = '/home/bahan'
V_PREFIX = os.popen("vserver-info APPDIR SYSINFO | grep \"prefix:\" | cut -d \":\" -f2").read().strip()
V_ROOTDIR = os.popen("vserver-info APPDIR SYSINFO | grep \"Rootdir:\" | cut -d \":\" -f2").read().strip()
V_CONFDIR = os.path.join(V_PREFIX,'etc/vservers')
API_DIR = os.getcwd()
ALL_IP = [ "192.168.70."+str(x)+"" for x in range(2,255)]
HOSTNAME = socket.gethostname()

class Vps:
    on_server = False
    
    # fungsi untuk menginisasi virtual private server. Apabila VPS yang dimaksud tidak ada
    # di dalam Host server, maka attribut on_server akan bernilai False.
    
    def get(self,nama):
	#scan Vserver-Rootdir untuk mengetahui semua Vps yang ada
	vps_list = os.listdir(V_ROOTDIR)
	vps_list.remove('.pkg')
	#membandingkan apakah nama VPS yang akan dibuat sudah ada atau belum 
	if nama in vps_list :
	    self.on_server = True
	    self.nama = nama
	else :
	    self.on_server = False
	    self.nama = nama
	    
	    
			
    def get_conf(self):
        if self.on_server == True :
            vdir = os.path.join(V_CONFDIR,self.nama)
            raw_mem = open(vdir+'/rlimits/rss.hard','r').read().strip()
            self.ip = open(vdir+'/interfaces/0/ip','r').read().strip()
            self.memory = str(int(raw_mem)/250)
        elif self.on_server == False :
            return "VPS %s tidak ada" % self.nama 
	    
	    
    def commit_conf(self):
        if self.on_server == True :
            ip = self.ip 
            mem = str(int(self.memory)*250)
            vdir = os.path.join(V_CONFDIR,self.nama)
            ip_hendler = open(vdir+'/interfaces/0/ip','w')
            ip_hendler.write(ip)
            ip_hendler.close()
                    
            mem_hendler = open(vdir+'/rlimits/rss.hard','w')
            mem_hendler.write(mem)
            mem_hendler.close()
        elif self.on_server == False :
            return "VPS %s tidak ada" % self.nama
	
	
    def destroy(self):
        shutil.rmtree(os.path.join(V_CONFDIR,self.nama))
        shutil.rmtree(os.path.join(V_ROOTDIR,self.nama))
	print "VPS dengan nama %s telah kami lenyapkan" % self.nama
		
	
	    
    def get_snap(self):
	pass
	
	
    def get_stat(self):
	pass

class VpsServer:	
    vps_obj= []

    def fetch_all(self):
	vps_list = os.listdir(V_ROOTDIR)
	vps_list.remove('.pkg')
	for vps in vps_list :
	    VPS = Vps()
	    VPS.get(vps)
	    VPS.get_conf()
	    self.vps_obj.append(VPS)
	    
    def get_available_ip(self):
	vps_list = os.listdir(V_ROOTDIR)
	vps_list.remove('.pkg')
	for vps in vps_list :
	    VPS = Vps()
	    VPS.get(vps)
	    if VPS.on_server :
		VPS.get_conf()
		ALL_IP.remove(VPS.ip)
	
	return ALL_IP
		
			

class VpsFactory:
    vps_server = VpsServer()
    ip = None
    ip_list = vps_server.get_available_ip()
    memory = None
    nama = None
		
    def valid_ip(self,ip):
	if ip in self.ip_list :
	    return True
	else : 
	    return False
	    
    def create_vps(self,ip,name,memory):
	vps_hostname = HOSTNAME.__add__("."+name+"")
	interface = "eth0:"+ip+"/24"
	home = os.path.join(V_ROOTDIR,name)
	conf = os.path.join(V_CONFDIR,name)
	base = V_BASEPKG.__add__("/*.t?z") 
	command = """
		   vserver %s build -m skeleton \
		   --hostname %s \
		   --interface %s \
		   --flags lock,virt_mem,virt_uptime,virt_cpu,virt_load,hide_netif\
		   --initstyle sysv
		  """ % (name,vps_hostname,interface)
	initcontent = """
		      #!/bin/bash
                      if [ "$1" == "3" ]; then
                         /etc/rc.d/rc.M
                      elif [ "$1" == "6" ]; then
                         /etc/rc.d/rc.6
                      else
                         echo "Invalid level."
                         exit 1
                      fi
		      """
	
	os.popen(command)
	
	os.mkdir(os.path.join(conf,'rlimits'))
	mem = open(os.path.join(conf,'rlimits/rss.hard'),'w')
	mem.write(""+str(int(memory)*250)+"\n")
	mem.close()
	
	os.system("/sbin/installpkg -root "+home+" "+base+"") 
	
	shutil.copy('/etc/localtime',os.path.join(home,'etc/localtime'))
	
	hname = open(os.path.join(home,'etc/HOSTNAME'),'w')
	hname.write(vps_hostname)
	hname.close()
	
	open(os.path.join(home,'etc/fstab'),'w').close()
	open(os.path.join(home,'etc/mtab'),'w').close()
	
	hosts = open(os.path.join(home,'etc/hosts'),'a')
	hosts.write(""+ip+" "+vps_hostname+" "+name+" ")
	hosts.close()

	init = open(os.path.join(home,'etc/init.d/rc'),'w')
	init.write(initcontent)
	init.close()
	init_file = os.path.join(home,'etc/init.d/rc')
	os.system("chmod +x "+init_file+"")
	
	change_sshd_config(home,ip)
	
	os.chdir(os.path.join(home,'etc/rc.d'))
	os.system("patch -p 1 < "+os.path.join(API_DIR,'slackware.patch')+"") 
	
	
    def save(self):
	if self.valid_ip(self.ip):
	    self.create_vps(self.ip,self.name,self.memory)
	else :
	    print "may be you must change name or ip of new VPS , couse your desire name for vps already taken !"
    
    

			