#!/bin/sh
export ALSADEV="plughw:1,0"
/home/pi/julius/julius-4.4.2.1/julius/julius -C /home/pi/julius/julius-4.4.2.1/julius-kit/grammar-kit-4.3.1/testmic.jconf -charconv UTF-8 UTF-8 -module &
wait 2
python3 talking2.py
echo END