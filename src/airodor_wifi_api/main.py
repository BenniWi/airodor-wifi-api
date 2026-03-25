import ipaddress

from airodor_wifi_api import airodor

if __name__ == "__main__":
    mode = airodor.get_mode(host=str(ipaddress.ip_address("192.168.2.122")), port=80, group=airodor.VentilationGroup.A)
    print(mode)
