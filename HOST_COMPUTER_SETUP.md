#Host Computer Setup

Authors:

    Peter Polidoro <polidorop@janelia.hhmi.org>

License:

    BSD

##Acer Aspire E 11 Laptop

Insert Xubuntu64 USB stick.

Insert ethernet cable.

Restart the computer.

Press the F2 key to enter computer's BIOS Setup during Power-On
Self-Test, or POST, process while the Acer logo is being displayed.

Press the Right Arrow key to select Main.

Select F12 Boot Menu.

Press the Enter key.

Select Enabled.

Press the Enter key.

Press the Right Arrow key to select Boot.

Use F6 to bring USB HDD to top of boot priority list.

Press F10 to Save and Exit.

##Boot Into Xubuntu Before Installing

Open a terminal.

```shell
sudo gparted
```

Delete all harddrive partitions and apply.

##Install Xubuntu

Download updates while installing.

Install third-party software.

Erase disk and install Xubuntu.

##Setup Secure Boot

Restart the computer.

Press the F2 key to enter computer's BIOS Setup during Power-On
Self-Test, or POST, process while the Acer logo is being displayed.

Press the Right Arrow key to select Security.

Set Supervisor password.

Select an UEFI file as trusted for executing.

Scroll through filesystem and select enable the 3 efi files inside
(shimx64.efi, grubx64.efi and mokmanager.efi) - be sure to type
exactly Yes (not yes) for confirmation for all 3 files.

Press F10 to Save and Exit.

##Setup Xubuntu

Open terminal.

```shell
sudo apt-get update
sudo apt-get dist-upgrade
sudo apt-get install git
mkdir ~/git
cd ~/git
git clone https://github.com/peterpolidoro/home.git
cd home
python symlinks.py -i -p -f
sudo reboot
```
