# WireGuard On-Demand (DigitalOcean)
### (based on angristan/wireguard-install)
  
Will spin up a DigitalOcean server and install and configure WireGuard.  
It then configures your local (client) computer to use this VPN.  
  
Assumes you are using **Ubuntu** and have already installed WireGuard.  
(https://www.wireguard.com/install/)  
  
* This requires python-digitalocean, I recommend a virtualenv.
* Also, resolvconf (sudo apt update && sudo apt install resolvconf)
* You need to put your DigitalOcean API personal access token in secret.py
* Then run python ./demo.py as root.
  
### N.B. These scripts are for testing purposes only! It is important to manually check all DigitalOcean instances created have been destroyed (or you will be paying for them!).  
### Also, it's possible these scripts may mess-up your network config, so use at your own risk!
