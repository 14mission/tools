#!/usr/bin/env bash
convert $1 -colorspace gray -fill '#063heisdwg.png' -colorize 50 /tmp/greengb.png
gsettings set org.cinnamon.desktop.background picture-uri file:///tmp/greengb.png
