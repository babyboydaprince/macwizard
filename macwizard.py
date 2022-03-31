from pyfiglet import Figlet
from termcolor import colored
from argparse import ArgumentParser
import subprocess
import os

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

parser = ArgumentParser(description='macchanger [Option] ', usage='python3 macchanger --help',
                        epilog='[ Set Manually ] python3 macwizard.py -i [interface] -m [YY:YY:YY:YY:YY:YY]')

rparser = parser.add_argument_group('Required Arguments:')

rparser.add_argument('-i', '--interface', dest='iface', metavar='',
                     type=str, help='iface you want to change the MAC')
rparser.add_argument('-m', '--mac', dest='newmac', metavar='',
                     type=str, help='MAC address to change MANUALLY')
rparser.add_argument(
    '-s', '--show', help='Show available ifaces and exit script', action='store_true')
parser.add_argument(
    '-R', '--Random', help='Generate a random MAC', action='store_true')

args = parser.parse_args()


def changemac():
    if ((args.iface) and (args.newmac)):
        subprocess.call(['sudo', 'ifconfig', args.iface, 'down'])
        subprocess.call(['sudo', 'ifconfig', args.iface,
                        'hw', 'ether', args.newmac])
        subprocess.call(['sudo', 'ifconfig', args.iface, 'up'])
        subprocess.call(['macchanger', '-s', args.iface])
    elif((args.iface) and (args.Random)):
        subprocess.call(['sudo', 'ifconfig', args.iface, 'down'])
        subprocess.call(['sudo', 'macchanger', '-r', args.iface])
        subprocess.call(['sudo', 'ifconfig', args.iface, 'up'])
    elif args.reset:
        subprocess.call(['sudo', 'ifconfig', args.iface, 'down'])
        subprocess.call(['sudo', 'ifconfig', '-p', args.iface])
        subprocess.call(['sudo', 'ifconfig', args.iface, 'up'])
    elif args.show:
        print('[:Available interface:]')
        os.system("sudo netstat -i | awk '{print $1}' > .test.txt")
        os.system('echo ------------- >> .test.txt')
        subprocess.call(['tail', '-n', '+3', '.test.txt'])
        subprocess.call(['sudo', 'rm', '-rf', '.test.txt'])
    else:
        subprocess.call(['python3', 'macwizard.py', '-h'])


if __name__ == '__main__':
    changemac()
