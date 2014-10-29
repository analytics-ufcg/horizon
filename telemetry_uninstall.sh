#!/bin/bash
echo 'Deletando arquivos...'

rm ../openstack_dashboard/api/telemetry.py

rm -r ../openstack_dashboard/api/telemetry_api

rm -r ../messages

cp ../telemetry_uninstall/_header.hmtl ../openstack_dashboard/templates

rm -r ../openstack_dashboard/dashboards/project/messages

rm ../horizon/static/horizon/js/c3.min.js

rm -r ../openstack_dashboard/dashboards/admin/graphs

rm -r ../openstack_dashboard/dashboards/admin/recommendations

rm -r ../openstack_dashboard/dashboards/admin/alarms

rm -r ../openstack_dashboard/dashboards/admin/benchmark

rm -r ../openstack_dashboard/dashboards/admin/messages

rm -r ../openstack_dashboard/dashboards/admin/sent_messages

cp ../telemetry_uninstall/dashboards.py ../openstack_dashboard/dashboards/admin

cp ../telemetry_uninstall/settings.py ../openstack_dashboard

rm ../horizon/static/horizon/js/d3.min.js

rm ../horizon/static/horizon/js/highcharts.js

rm ../horizon/static/horizon/js/highcharts-more.js

cp ../telemetry_uninstall/_scripts.html ../horizon/templates/horizon

cp ../telemetry_uninstall/_stylesheets.html ../openstack_dashboard/templates

rm ../openstack_dashboard/static/dashboard/less/c3.css

echo 'Arquivos deletados.'

#apagar os bds e tabelas tambem

rm -r ../telemetry_uninstall 
