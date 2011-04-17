# -*- coding: iso-8859-1 -*-
import os

V_BASEPKG = '/home/bahan'
V_PREFIX = os.popen("vserver-info APPDIR SYSINFO | grep \"prefix:\" | cut -d \":\" -f2").read().strip()
V_ROOTDIR = os.popen("vserver-info APPDIR SYSINFO | grep \"Rootdir:\" | cut -d \":\" -f2").read().strip()
V_CONFDIR = os.path.join(V_PREFIX,'etc/vservers/')
