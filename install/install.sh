#!/bin/sh
sudo pacman -R python-pyqt5 pyqt5-common 
sudo pacman -Syu
sudo pacman -S vim hdf5 opencv scrot
sudo pacman -S fcitx-gtk3 fcitx-chewing fcitx-configtool fcitx
echo export GTK_IM_MODULE=fcitx >> ~/.xprofile
echo export QT_IM_MODULE=fcitx >> ~/.xprofile
echo XMODIFIERS=@im=fcitx >> ~/.xprofile
echo alias vi='vim' >> ~/.bashrc
sudo mkdir .tmp_pip
sudo -H pip install -b .tmp_pip spyder numpy Xlib
sudo -H pip install -b .tmp_pip requests pillow mss lxml beautifulsoup4 pyautogui
sudo rm -rf .tmp_pip
