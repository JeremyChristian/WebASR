from fabric.api import *
from django.utils import timezone
from datetime import *

env.user="webasr"
env.hosts=["squeal.dcs.shef.ac.uk"]

env.password="asr4daweb"


def process_execute(localpath,filename,channels,command):

	put(localpath,'/share/spandh.ami1/srv/webasr/filestore/input/201507/')
	with cd('/share/spandh.ami1/srv/webasr'):
		run('mkdir proc/'+filename+' proc/'+filename+'/data')
		run('touch proc/'+filename+'/'+filename+'.cfg')
		run('touch proc/'+filename+'/'+filename+'.dal')
		with cd('proc/'+filename):
			run("echo '[Execute]' >> "+filename+'.cfg')
			run("echo 'Priority = 0' >> "+filename+'.cfg')
			for x in range(1,(int(channels)+1)):
				run("echo '"+filename+'_chn-'+(('0000'+str(x))[-5:])+"' >> "+filename+'.dal')
				with cd('data/'):	
					run('ln -s /share/spandh.ami1/srv/webasr/filestore/input/201507/'+filename+'.wav '+filename+'_chn-'+(('0000'+str(x))[-5:])+'.audio')
	run(command+' '+filename)
