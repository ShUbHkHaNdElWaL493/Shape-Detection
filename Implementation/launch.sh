#!/bin/bash

gnome-terminal -- roscore
sleep 1

command1="/bin/bash camera_publisher.sh"
gnome-terminal -- $command1
sleep 1

command2="/bin/bash image_processor.sh"
gnome-terminal -- $command2
sleep 1

rviz