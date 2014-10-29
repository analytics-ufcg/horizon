#!/bin/bash
mkdir telemetry_temp
echo 'Fazendo download dos arquivos...'

git clone https://github.com/analyticsUfcg/horizon telemetry_temp

echo 'Download de arquivos concluido.'

mkdir telemetry_uninstall

echo 'Copiando arquivos...'

cp telemetry_temp/openstack_dashboard/api/telemetry.py openstack_dashboard/api

cp -r telemetry_temp/openstack_dashboard/api/telemetry_api openstack_dashboard/api

cp -r telemetry_temp/messages .

cp openstack_dashboard/templates/_header.html telemetry_uninstall

cp telemetry_temp/openstack_dashboard/templates/_header.html openstack_dashboard/templates

cp -r telemetry_temp/openstack_dashboard/dashboards/project/messages openstack_dashboard/dashboards/project

cp telemetry_temp/horizon/static/horizon/js/c3.min.js horizon/static/horizon/js

cp -r telemetry_temp/openstack_dashboard/dashboards/admin/graphs openstack_dashboard/dashboards/admin

cp -r telemetry_temp/openstack_dashboard/dashboards/admin/recommendations openstack_dashboard/dashboards/admin

cp -r telemetry_temp/openstack_dashboard/dashboards/admin/alarms openstack_dashboard/dashboards/admin

cp -r telemetry_temp/openstack_dashboard/dashboards/admin/benchmark openstack_dashboard/dashboards/admin

cp -r telemetry_temp/openstack_dashboard/dashboards/admin/messages openstack_dashboard/dashboards/admin

cp -r telemetry_temp/openstack_dashboard/dashboards/admin/sent_messages openstack_dashboard/dashboards/admin

cp openstack_dashboard/dashboards/admin/dashboard.py telemetry_uninstall

cp telemetry_temp/openstack_dashboard/dashboards/admin/dashboard.py openstack_dashboard/dashboards/admin

cp openstack_dashboard/settings.py telemetry_uninstall

cp telemetry_temp/openstack_dashboard/settings.py openstack_dashboard

cp telemetry_temp/horizon/static/horizon/js/d3.min.js horizon/static/horizon/js

cp telemetry_temp/horizon/static/horizon/js/highcharts.js horizon/static/horizon/js

cp telemetry_temp/horizon/static/horizon/js/highcharts-more.js horizon/static/horizon/js

cp horizon/templates/horizon/_scripts.html telemetry_uninstall

cp telemetry_temp/horizon/templates/horizon/_scripts.html horizon/templates/horizon

cp openstack_dashboard/templates/_stylesheets.html telemetry_uninstall

cp telemetry_temp/openstack_dashboard/templates/_stylesheets.html openstack_dashboard/templates

cp telemetry_temp/openstack_dashboard/static/dashboard/less/c3.css openstack_dashboard/static/dashboard/less

echo 'Arquivos copiados.'

echo 'Instalando dependencias...'

#pip install httplib2

#pip install mysql-python

#pip install numpy

#pip install oslo.config

echo 'Dependencias instaladas.'

python manage.py syncdb

cp telemetry_temp/telemetry_uninstall.sh telemetry_uninstall

rm -r telemetry_temp
