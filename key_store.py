import subprocess
import tempfile
from pathlib import Path
import digitalocean as do
from secret import token

class KeyStore(object):
   def __init__(self, key_name='key'):

      tmp_dir = tempfile.TemporaryDirectory()
      self._persist_tmp_dir = tmp_dir

      tmp_path = Path(tmp_dir.name)
      prv_key_path = tmp_path/key_name
      self.prv_key_pathstr = prv_key_path.as_posix()

      cmd = ['ssh-keygen',
             '-t', 'ed25519',
             '-a', '123',
             '-f', self.prv_key_pathstr,
             '-C', 'VPN',
             '-N', '']
      subprocess.check_output(cmd)

      pub_key_path = tmp_path/(key_name+'.pub')
      pub_key_path.chmod(0o600)
      pub_key = pub_key_path.open().read()

      pub_do_key = do.SSHKey(token=token, name=key_name, public_key=pub_key)
      pub_do_key.create()
      self.pub_do_key = pub_do_key

   def __del__(self):
      print('Destroying pub_do_key')
      self.pub_do_key.destroy()
