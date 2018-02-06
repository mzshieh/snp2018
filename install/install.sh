#!/bin/sh
sudo pacman -R python-pyqt5
sudo pacman -Syu
sudo pacman -S vim hdf5 opencv scrot python-xlib
sudo mkdir .tmp_pip
sudo -H pip install -b .tmp_pip spyder pillow mss lxml beautifulsoup4
sudo -H pip install -b .tmp_pip pyautogui
sudo rm -rf .tmp_pip
