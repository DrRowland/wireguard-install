import subprocess
from pathlib import Path

class SSHTools(object):
   def __init__(self, server):
      self.server = server

   def ssh(self, cmd):
      args = ['ssh',
              '-o', 'StrictHostKeyChecking=no',
              '-o', 'UserKnownHostsFile=/dev/null',
              '-o', 'LogLevel ERROR',
              '-i', self.server.key_store.prv_key_pathstr,
              'root@'+self.server.droplet.ip_address,
              cmd]
      subprocess.run(args)

   def sftp(self, cmd):
      args = ['sftp',
              '-o', 'StrictHostKeyChecking=no',
              '-o', 'UserKnownHostsFile=/dev/null',
              '-o', 'LogLevel ERROR',
              '-i', self.server.key_store.prv_key_pathstr,
              'root@'+self.server.droplet.ip_address]
      p = subprocess.Popen(args, stdin=subprocess.PIPE)
      p.communicate(cmd.encode('UTF-8'))
      p.stdin.close()
      p.wait()

   def install_wireguard(self):
      self.sftp('put ./wireguard-install.sh')
      self.ssh('bash ./wireguard-install.sh --auto')

   def allow_password_login(self):
      self.ssh('sed -i \'s/PasswordAuthentication no'+
                         '/PasswordAuthentication yes/g\' '+
                         '/etc/ssh/sshd_config')
      self.ssh('service ssh restart')

   def add_user(self, username, password):
      self.ssh('useradd -m -p $(openssl passwd -crypt '+password+') -s /bin/bash '+username)

