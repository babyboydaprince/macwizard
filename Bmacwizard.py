from pyfiglet import Figlet
from termcolor import colored
import parser
import subprocess
import string
import random
import re

dona = """
===================== Made by BraiNiac ==================
===================== Buy me a beer :) ==================
==== BTC: bc1q8z64uky7jgwdsygc7fwq97d4u8yfr8hj57s200 ====
=========================================================
"""
f = Figlet(font='banner3-D')

print(colored(f.renderText('Mac'), 'red'))
print(colored(f.renderText('Wizard'), 'green'))

print(dona)


def randomize():
    """Generate and return a MAC address (linux) format"""
    # get the hexdigits uppercased
    uppercase_hex = ''.join(set(string.hexdigits.upper()))
    # 2nd char must be 0, 2, 6, 8, A, C, or E
    mac = ""
    for i in range(6):
        for j in range(2):
            if i == 0:
                mac += random.choice("02468ACE")
            else:
                mac += random.choice(uppercase_hex)
        mac += ":"
    return mac.strip(":")


def get_mac(iface):
    # use ifconfig command to get iface details, including MAC address
    output = subprocess.check_output(f"ifconfig {iface}", shell=True).decode()
    return re.search("ether (.+) ", output).group().split()[1].strip()


def change_mac(iface, new_mac):
    # disable network iface
    subprocess.check_output(f"ifconfig {iface} down", shell=True)
    # change the MAC
    subprocess.check_output(f"ifconfig {iface} hw ether {new_mac}", shell=True)
    # enable network iface back up
    subprocess.check_output(f"ifconfig {iface} up", shell=True)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Python MAC Changer for Linux")
    parser.add_argument(
        "interface", help='The network interface name on Linux')
    parser.add_argument("-r", "--random", action="store_true",
                        help='In order to generate a random MAC address')
    parser.add_argument(
        '-m', '--mac', help='Insert manually the MAC you want to change to')
    args = parser.parse_args()
    iface = args.interface

    if args.random:
        # if random parameter is set, generate a random MAC
        new_mac = randomize()
    elif args.mac:
        # if mac is set, uset it instead
        new_mac = args.mac
    # get current MAC address
    old_mac = get_mac(iface)
    print("[*] Old MAC address: ", old_mac)
    # change the MAC
    change_mac(iface, new_mac)
    # chack if mac was changes
    new_mac = get_mac(iface)
    print("[+] New MAC address: ", new_mac)
