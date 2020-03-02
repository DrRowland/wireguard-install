from wg_tools import WG

wg = WG()

wg.start()
print()
print('IP: '+wg.tools.server.droplet.ip_address)
input('Press enter to stop using the VPN (and delete it)')
wg.stop()

