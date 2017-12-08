#!/bin/bash


lastSong=$(playerctl metadata mpris:trackid)
while true; do
	song=$(playerctl metadata mpris:trackid)
	if [ "$song" != "$lastSong" ]
	then 
		echo "Changed"
		lastSong=$song
	fi


done
