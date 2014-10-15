CREATE TABLE hosts_data_table(
     id MEDIUMINT NOT NULL AUTO_INCREMENT,
     Date TIMESTAMP, 
     Cpu_Util FLOAT(5,2), 
     Memory VARCHAR(150), 
     Disk VARCHAR(200), 
     Host VARCHAR(20), 
     PRIMARY KEY (id)
);
