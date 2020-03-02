import subprocess
from pathlib import Path
from key_store import KeyStore
from do_server import DOServer
from ssh_tools import SSHTools

class WG(object):
   
   def __init__(self):
      tools = SSHTools(DOServer(KeyStore()))
      tools.install_wireguard()
      tools.allow_password_login()
      tools.add_user('username', 'changeme')
      tools.sftp('get ./wg0-client.conf')
      Path('./wg0-client.conf').rename('/etc/wireguard/wg0-client.conf')
      self.tools = tools

   def start(self):
      cmd = ['wg-quick',
             'up',
             'wg0-client']
      subprocess.run(cmd)

   def stop(self):
      cmd = ['wg-quick', 
             'down', 
             'wg0-client']
      subprocess.run(cmd)

   def __del__(self):
      Path('/etc/wireguard/wg0-client.conf').unlink()

