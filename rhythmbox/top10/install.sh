#!/bin/bash

if [ "$UID" -ne 0 ] 
then
    echo "Must be root to run this."
    # non root exit error
    exit 87
else
    echo "Installing..."
    sleep 3
    cp rhythmbox.plugin.top10.gschema.xml /usr/share/glib-2.0/schemas/
    glib-compile-schemas /usr/share/glib-2.0/schemas
    mkdir -p $HOME/.local/share/rhythmbox/plugins/top10
    cp -r * $HOME/.local/share/rhythmbox/plugins/top10
    rm  $HOME/.local/share/rhythmbox/plugins/top10/*.sh
    echo "plugins installed sucess!...enjoy!"
fi
