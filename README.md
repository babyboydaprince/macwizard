# MAC WIZARD - mac changer made with python 3

Python script which changes the network interface mac address.

![alt text](https://github.com/babyboydaprince/macwizard/blob/main/img/logo.png?raw=true)

## 🚀 Run

```
[Set Manually] python macwizard.py -i [interface] -m YY:YY:YY:YY:YY:YY
```

```
[Auto] python macwizard.py -i [interface] -R
```

### 📋 Prerequisites

- Python 3


### 🔧  MACWIZARD Installation (LINUX)
```
pip install -r requirements.txt
```
```
python macwizard.py -h
```
```
-s Show available interfaces
-m  Manual mode
-r  reset to original MAC
-h  help
-R  Automatically pick random MAC for your interface
-i  Interface
```
## MACWIZARD4WIN Installation (WINDOWS)

## Binaries
Compatible with Win 7/Vista/8/10 32/64bit.

If you want to create your own executable, generate it with [Pyinstaller](https://www.pyinstaller.org/) on a Win 7/Vista/8/10 32/64bit system:
```
pyinstaller macwizard4win.py -F --clean
```

## MACWIZARD4WIN Usage:
CMD or PowerShell with administrative privileges. Most use cases can be found in the 'Example usage' section:
```
macwizard4win.py -h

usage: macwizard4win.exe [-h] [-l] [-r] [-i INTERFACE] [-m MAC] [-f]

A small script to change MAC addresses in Windows

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            list all network interfaces
  -r, --reset           reset MAC address of the provided network interface to
                        default
  -i INTERFACE, --interface INTERFACE
                        provide an interface GUID (part of the "Transport
                        Name"), e.g. CA8D7884-4754-4E6D-B637-D411533ECBBA
  -m MAC, --mac MAC     provide a valid MAC address, e.g. 00:0C:29:FE:8B:77.
                        Might need 02 as the first octet for Wifi.
  -f, --force           force restart network interface

Note:
WiFi Connections might need a 02 as first octet, e.g. 02:xx:xx:xx:xx:xx

Example usage:
change-mac.exe -l
change-mac.exe -i CA8D7884-4754-4E6D-B637-D411533ECBBA -m 00:0C:29:FE:8B:77
change-mac.exe -i CA8D7884-4754-4E6D-B637-D411533ECBBA -m 00:0C:29:FE:8B:77 -f
change-mac.exe -i CA8D7884-4754-4E6D-B637-D411533ECBBA -r
change-mac.exe -i CA8D7884-4754-4E6D-B637-D411533ECBBA -f
change-mac.exe -i CA8D7884-4754-4E6D-B637-D411533ECBBA -r -f
```

## 🛠️ Made with

- Python 3.9.13


## 📌 Macwizard version

- 1.1

---

## 📌 Macwizard 4 Win

- beta (available)

---

⌨️ Made with ❤️ by [BraiNiac](https://github.com/babyboydaprince) 👽
