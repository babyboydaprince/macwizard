import subprocess
import regex as re
import string
import random


# registry path of network interfaces
network_interface_reg_path = r'HKEY_LOCAL_MACHINE\\SYSTEM\\' \
    'CurrentControlSet\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}'
# transport name regular expression, looks like
# {AF1B45DB-B5D4-46D0-B4EA-3E18FA49BF5F}
transport_name_regex = re.compile("{.+}")
# MAC address regular expression
mac_address_regex = re.compile(r"([A-Z0-9]{2}[:-]){5}([A-Z0-9]{2})")


def get_random_mac():
    """Generate and return a MAC address in WINDOWS format"""
    # get the hexdigits in uppercase
    upper_hexdigits = ''.join(set(string.hexdigits.upper()))
    # 2nd character must be 2, 4, A, or E
    return random.choice(upper_hexdigits) \
        + random.choice("24AE") \
        + "".join(random.sample(upper_hexdigits, k=10))


def clean_mac(mac):
    """ Function to clean non hexadecimal characters from a MAC address
    mostly used to remove '-' and ':' from MAC addresses and return it
    in uppercase"""
    return "".join(c for c in mac if c in string.hexdigits).upper()


def get_connected_adapters_mac_address():
    # make a list to collect connected adapter's
    # MAC addresses along with the transport name
    connected_adapters_mac = []
    # use the getmac command to extract
    for potential_mac in subprocess.check_output(
            "getmac").decode().splitlines():
        # parse the MAC address from the line
        mac_address = mac_address_regex.search(potential_mac)
        # parse the transport name from the line
        transport_name = transport_name_regex.search(potential_mac)
        if mac_address and transport_name:
            # if a MAC and transport name are found,
            # add them to our list
            connected_adapters_mac.append(
                (mac_address.group(), transport_name.group()))
    return connected_adapters_mac


def get_user_adapter_choice(connected_adapters_mac):
    # print the available adapters
    for i, option in enumerate(connected_adapters_mac):
        print(f"#{i}: {option[0]}, {option[1]}")
    if len(connected_adapters_mac) <= 1:
        # when there is only one adapter, choose it immediately
        return connected_adapters_mac[0]
    # prompt the user to choose a network adapter index
    try:
        choice = int(
            input("Choose the interface you want to change the MAC address:"))
        # return the target chosen adapter's
        # MAC and transport name that we'll use later
        # to search for our adapter using the reg QUERY command
        return connected_adapters_mac[choice]
    except:
        # if -for whatever reason- an error is raised,
        # just quit the script
        print("Not a valid choice, exiting...")
        exit()
