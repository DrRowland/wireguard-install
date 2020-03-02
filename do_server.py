import subprocess
from time import sleep
import digitalocean as do
from secret import token

class DOServer(object):
   def __init__(self, key_store, server_name='VPN'):
      droplet = do.Droplet(
         token=token,
         name=server_name,
         region='lon1', #London
         image='debian-9-x64', #Debian 9.5 x64
         size_slug='s-1vcpu-1gb',  # $5 per month
         ssh_keys=[key_store.pub_do_key],
         backups=False)
      droplet.create()

      manager = do.Manager(token=token)
      while droplet.ip_address is None:
         print('Waiting for ip address...')
         sleep(5)
         droplet = manager.get_droplet(droplet.id)
      print(droplet.ip_address)

      check_str = 'Pause for port'
      cmd = ['ssh',
             '-o', 'StrictHostKeyChecking=no',
             '-o', 'UserKnownHostsFile=/dev/null',
             '-o', 'ConnectTimeout=10',
             '-o', 'LogLevel ERROR',
             '-i', key_store.prv_key_pathstr,
             'root@'+droplet.ip_address,
             'echo '+check_str]
      port_available = False
      while not port_available:
         print('Waiting for port...')
         sleep(5)
         try:
            output = subprocess.check_output(cmd)
            if output == (check_str+'\n').encode('UTF-8'):
               port_available = True
         except subprocess.CalledProcessError as e:
            pass

      self.droplet = droplet
      self.key_store = key_store

   def __del__(self):
      print('Destroying droplet')
      self.droplet.destroy()

