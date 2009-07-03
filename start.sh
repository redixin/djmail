#!/bin/sh

self="${0#./}"
base="${self%/*}"
current=$(pwd)

if [ "$base" = "$self" ] ; then
cd "$current"
else
cd "$base"
fi ;

exec sudo -u mail ./manage.py runfcgi socket=/tmp/djmail.sock daemonize=false
