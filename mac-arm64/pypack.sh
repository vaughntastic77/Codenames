#!/bin/bash

pyinstaller main.py -F -w --add-data "../assets:assets" --add-data "../assets/images:assets/images" -i "../assets/images/icon.png" -n "Codenames"
