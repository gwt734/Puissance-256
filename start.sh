#!/bin/bash
if command -v python
then
    python main.py
    echo python

else
    if command -v python3
    then
        echo python3
    else
        notify-send -u critical "You need to install python3"
        exit 1
    fi
fi
if command -v pip
then
    if pip show pygame
    then
        if pip show screeninfo
        then
            python3 main.py
        else
            notify-send -u critical "You need to install screeninfo"
        fi
    else
        notify-send -u critical "You need to install pygame"
    fi
else
    notify-send -u critical "You need to install pip"
fi