CREATE TABLE hosts_data_table(
     id MEDIUMINT NOT NULL AUTO_INCREMENT,
     Date TIMESTAMP, 
     Cpu_Util FLOAT(5,2), 
     Memory VARCHAR(150), 
     Disk VARCHAR(200), 
     Network VARCHAR(200),
     Host VARCHAR(20), 
     ServiceStatus VARCHAR(2000),
     HostStatus CHAR(1) DEFAULT 'T',
     PRIMARY KEY (id)
);
