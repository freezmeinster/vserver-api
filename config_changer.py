import re,os,shutil


def change_sshd_config(confdir,ip):
    old_path = os.path.join(confdir,'etc/ssh/sshd_config')
  
    file = open(old_path,'r+')
    line = file.readlines()	
    b = []

    for l in line :
	if l.startswith("#ListenAddress 0.0.0.0"):
	    linenew = re.sub("#ListenAddress 0.0.0.0" ,"ListenAddress "+ip+"" ,l)
	    b.append(linenew)
	b.append(l)
	
    shutil.move(old_path,os.path.join(confdir,'etc/ssh/sshd_config_old'))
    new_conf = open(os.path.join(confdir,'etc/ssh/sshd_config'),'w')
    
    for line in b :
	new_conf.write(line)
	
    new_conf.close()