#!/bin/bash

cp install/magic.mime /etc/magic.mime
cp install/deb/jukeberry.service /lib/systemd/system/jukeberry.service
systemctl enable jukeberry.service
cp /etc/jukeberry.example.conf /etc/jukeberry.conf
chmod a+r /etc/jukeberry.conf

