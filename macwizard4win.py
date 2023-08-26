# Created by BraiNiac
import subprocess
import sys
import argparse
import regex as re
import string
import random
from pyfiglet import Figlet
from termcolor import colored

"""BANNER"""

f = Figlet(font='banner3-D')
print('\n')
print(colored(f.renderText('Mac'), 'red'))
print(colored(f.renderText('Wizard'), 'green'))

# Registry path of network interfaces
net_interface_reg_path = (r"HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\"
                          r"Control\\Class\\{4d36e972-e325-11ce-bfc1-"
                          r"08002be10318}")

# Transport name regular expression, looks like
# {AF1B45DB-B5D4-46D0-B4EA-3E18FA49BF5F}
transport_name_regex = re.compile('{.+}')

# MAC address regular expression
mac_regex = re.compile(r"([A-Z0-9]{2}[:-]){5}([A-Z0-9]{2})")


# Generate a MAC address in the format of WINDOWS
def get_random_mac():
    upper_hexdigits = ''.join(set(string.hexdigits.upper()))

    return random.choice(upper_hexdigits) + random.choice('24AE')


# Simple function to clean non hexadecimal characters from a MAC address
def clear_mac(mac):
    return ''.join(c for c in mac if c in string.hexdigits).upper()


# Get the MAC address from available adapters
def connected_adapters_mac():
    adapters_mac = []

    for potential_mac in subprocess.check_output(
            'getmac').decode(encoding='iso8859-1').splitlines():

        mac_address = mac_regex.search(potential_mac)

        transport_name = transport_name_regex.search(potential_mac)

        if mac_address and transport_name:
            adapters_mac.append((mac_address.group(), transport_name.group()))

    return adapters_mac


# Choose an adapter to change de MAC
def adapter_choice(adapters_mac):
    for i, option in enumerate(adapters_mac):
        print(f'#{i}: {option[0]}, {option[1]}')

    if len(adapters_mac) <= 1:
        return adapters_mac[0]

    try:

        choice = int(input('Choose an interface to change the MAC address: '))

        return adapters_mac[choice]

    except Exception as err:

        print('Not a valid choice, exiting MACWIZARD...', err)


# Change MAC of given adapter
def change_mac(transport_name, new_mac):
    output = subprocess.check_output(f'reg QUERY ' +
                                     net_interface_reg_path.replace(
                                         '\\\\', '\\')).decode()

    for interface in re.findall(rf'{net_interface_reg_path}\\\d+', output):

        net_adapter_index = int(interface.split('\\')[-1])

        interface_content = subprocess.check_output(
            f'reg QUERY {interface.strip()}').decode()

        if transport_name in interface_content:
            mac_changed = subprocess.check_output(
                f'reg add {interface} /v NetworkAddress '
                f'/d {new_mac} /f').decode()

            print(mac_changed)

            break

        return net_adapter_index


"""TO-DO"""


# Restore original MAC address
# def restore_old_mac(interface_index):
#
#     winreg.DeleteValue(interface_index, 'NetworkAddress')


# Disable adapter -> necessary for reflecting changes
def disable_adapter(adapter_index_dis):
    disable_output = subprocess.check_output(
        f'wmic path win32_networkadapter where '
        f'index={adapter_index_dis} call disable').decode()

    return disable_output


# Enable adapter -> necessary for reflecting changes
def enable_adapter(adapter_index_en):
    enable_output = subprocess.check_output(
        f"wmic path win32_networkadapter where "
        f"index={adapter_index_en} call enable").decode()

    return enable_output


# Set arguments
parser = argparse.ArgumentParser(
    description="-- MACWIZARD -- Python MAC Changer 4Win")

parser.add_argument(
    "-r",
    "--randomize",
    action="store_true",
    help="Generate a random MAC address")

parser.add_argument(
    "-m",
    "--macaddress",
    help="The new MAC you want to change to")

# Get arguments
args = parser.parse_args()
randomize = args.randomize
macaddress = args.macaddress


""" MAIN RUNNER """
if __name__ == "__main__":
    try:

        # if not macaddress or not randomize:
        parser.print_help()
        print("\n")

        choice_mode = input(f'Choose work mode: ')

        if randomize == choice_mode:

            # Random
            connected_adapters = connected_adapters_mac()

            old_mac_address, target_transport_name = (
                adapter_choice(connected_adapters))
            print("[*] Old MAC address:", old_mac_address)

            new_mac_address = get_random_mac()

            adapter_index = change_mac(target_transport_name, new_mac_address)
            print("[+] Changed to:", new_mac_address)

            disable_adapter(adapter_index)

            print("[+] Adapter is disabled")

            enable_adapter(adapter_index)
            print("[+] Adapter is enabled again")
            print('Done.')

        elif macaddress == choice_mode:

            # Set
            new_mac_address = clear_mac(macaddress)

            adapter_index = change_mac(target_transport_name, new_mac_address)
            print("[+] Changed to:", new_mac_address)

            disable_adapter(adapter_index)

            print("[+] Adapter is disabled")

            enable_adapter(adapter_index)
            print("[+] Adapter is enabled again")
            print('Done.')

    except Exception as e:

        print('It must be some king of wizardry...\n', e)
        parser.print_help()
        sys.exit()
