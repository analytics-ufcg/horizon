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

#sudo apt-get install mysql

#sudo apt-get install libmysqlclient-dev

#.venv/bin/pip install httplib2

#.venv/bin/pip install mysql-python

#.venv/bin/pip install numpy

#.venv/bin/pip install oslo.config

echo 'Dependencias instaladas.'

echo 'Criando os bancos de dados.'

echo 'Digite a senha de root do mysql'

./create_bd.sh message_database telemetry_user 2910901b3537f1ecc45f

mysql -u telemetry_user -p2910901b3537f1ecc45f -e "create database hosts_data;"

mysql -u telemetry_user -p2910901b3537f1ecc45f -e "create database telemetry_benchmarks;"

mysql -D telemetry_benchmarks -u telemetry_user -p2910901b3537f1ecc45f -e "CREATE TABLE benchmark_history (
  id mediumint(9) NOT NULL AUTO_INCREMENT,
  timestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  host_address varchar(15) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8
;

CREATE TABLE cpu_table (
  id mediumint(9) NOT NULL DEFAULT 0,
  cpu_average_time float(7,2) DEFAULT NULL,
  cpu_median_time float(7,2) DEFAULT NULL,
  cpu_min_time float(7,2) DEFAULT NULL,
  cpu_max_time float(7,2) DEFAULT NULL,
  first_quarter_time float(7,2) DEFAULT NULL,
  second_quarter_time float(7,2) DEFAULT NULL,
  third_quarter_time float(7,2) DEFAULT NULL,
  fourth_quarter_time float(7,2) DEFAULT NULL,
  PRIMARY KEY (id),
  CONSTRAINT cpu_table_ibfk_1 FOREIGN KEY (id) REFERENCES benchmark_history (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

CREATE TABLE disk_table (
  id mediumint(9) NOT NULL DEFAULT 0,
  disk_average_time float(7,2) DEFAULT NULL,
  disk_median_time float(7,2) DEFAULT NULL,
  disk_min_time float(7,2) DEFAULT NULL,
  disk_max_time float(7,2) DEFAULT NULL,
  first_quarter_time float(7,2) DEFAULT NULL,
  second_quarter_time float(7,2) DEFAULT NULL,
  third_quarter_time float(7,2) DEFAULT NULL,
  fourth_quarter_time float(7,2) DEFAULT NULL,
  PRIMARY KEY (id),
  CONSTRAINT disk_table_ibfk_1 FOREIGN KEY (id) REFERENCES benchmark_history (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

CREATE TABLE mem_table (
  id mediumint(9) NOT NULL DEFAULT 0,
  mem_average_time float(7,2) DEFAULT NULL,
  mem_median_time float(7,2) DEFAULT NULL,
  mem_min_time float(7,2) DEFAULT NULL,
  mem_max_time float(7,2) DEFAULT NULL,
  first_quarter_time float(7,2) DEFAULT NULL,
  second_quarter_time float(7,2) DEFAULT NULL,
  third_quarter_time float(7,2) DEFAULT NULL,
  fourth_quarter_time float(7,2) DEFAULT NULL,
  PRIMARY KEY (id),
  CONSTRAINT mem_table_ibfk_1 FOREIGN KEY (id) REFERENCES benchmark_history (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

COMMIT;" 

mysql -D hosts_data -u telemetry_user -p2910901b3537f1ecc45f -e "CREATE TABLE hosts_data_table (
  id mediumint(9) NOT NULL AUTO_INCREMENT,
  Date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  Cpu_Util float(5,2) DEFAULT NULL,
  Memory varchar(150) DEFAULT NULL,
  Disk varchar(200) DEFAULT NULL,
  Host varchar(20) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=888937 DEFAULT CHARSET=utf8 
;

COMMIT;"

python manage.py syncdb

cp telemetry_temp/telemetry_uninstall.sh telemetry_uninstall

rm -r telemetry_temp
