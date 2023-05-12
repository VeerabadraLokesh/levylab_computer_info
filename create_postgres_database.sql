CREATE SCHEMA IF NOT EXISTS system_info;
DROP TABLE IF EXISTS system_info.storage_info;
DROP TABLE IF EXISTS system_info.system_info;


CREATE TABLE IF NOT EXISTS system_info.system_info(
MAC_addr                VARCHAR(20)			NOT NULL    PRIMARY KEY,
host_name               VARCHAR(50)         NOT NULL,
operating_system        VARCHAR(50)         NOT NULL,
CPU_model               VARCHAR(50)         NOT NULL,
update_timestamp        TIMESTAMP           NOT NULL,
ip_addr                 VARCHAR(50)         NOT NULL
);


CREATE TABLE IF NOT EXISTS system_info.storage_info(
MAC_addr                VARCHAR(20)			NOT NULL,
disk_partition          VARCHAR(5)          NOT NULL,
used                    VARCHAR(20)			NOT NULL,    
free                    VARCHAR(20)			NOT NULL,    
total                   VARCHAR(20)			NOT NULL,    
FOREIGN KEY(MAC_addr)
REFERENCES system_info.system_info(MAC_addr)
ON DELETE CASCADE
ON UPDATE CASCADE,
PRIMARY KEY(MAC_addr, disk_partition)
);
