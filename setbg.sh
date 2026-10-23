#!/usr/bin/env bash
convert $1 -colorspace gray -fill '#063heisdwg.png' -colorize 50 /tmp/greenbg.png
gsettings set org.cinnamon.desktop.background picture-uri file:///tmp/greenbg.png
