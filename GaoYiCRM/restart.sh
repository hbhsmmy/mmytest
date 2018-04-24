#!/bin/bash
killall -9 uwsgi
sleep 1s
sudo /etc/init.d/uwsgi --ini /webprd/CRMDjango/GaoYiCRM/mysite_uwsgi.ini > /webprd/CRMDjango/GaoYiCRM/uwsgi.txt
