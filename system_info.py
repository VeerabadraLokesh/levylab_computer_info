#!/usr/bin/python

import os
import socket
import platform
import uuid
import psycopg2 as psql
import shutil
import datetime
import logging
from time import sleep
from pathlib import Path


PSQL_DB_HOST = "192.168.1.215"
DATABASE_NAME = "levylab"
DATABASE_USERNAME = "postgres"

RECONNECT_INTERVAL = 10

q1 = "DELETE FROM system_info.storage_info WHERE mac_addr = %s;"
q2 = "DELETE FROM system_info.system_info WHERE mac_addr = %s;"
q3 = "INSERT INTO system_info.system_info VALUES(%s,%s,%s,%s,%s,%s);"
q4 = "INSERT INTO system_info.storage_info VALUES(%s,%s,%s,%s,%s);"

WINDOWS = 'WINDOWS'
LINUX = 'LINUX'
MAC = 'MAC OS'

BYTES_PER_GIB = 2**30

pgpass_conf_location = os.path.join(Path(__file__).parent.absolute(), "pgpass.conf")

class SystemInfo():
    def __init__(self):
        self.get_os_info()
        

    def get_os_info(self):
        self.operating_system = platform.system().upper()
        # print(f"Operating system: {self.operating_system}")
        logging.info(f"Operating system: {self.operating_system}")

        sys_info = platform.uname()
        self.sys_info = sys_info
        self.operating_system_info = sys_info.system + sys_info.version
        logging.info(f"Operating System info: {self.operating_system_info}")

        self.hostname = sys_info.node
        logging.info(f"Host name: {self.hostname}")

        self.processor_model = sys_info.machine
        logging.info(f"Processor model: {self.processor_model}")


    def get_network_info(self):
        self.ipv4_addr = socket.gethostbyname_ex(self.hostname)[2]
        if isinstance(self.ipv4_addr, list):
            self.ipv4_addr = self.ipv4_addr[0]
        logging.info(f"IPv4 address: {self.ipv4_addr}")

        self.mac_addr = (':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                for ele in range(0,8*6,8)][::-1]))

        logging.info(f"Mac address: {self.mac_addr}")
        

    def check_internet_connection(self):

        ping_result = -1

        try:
            logging.info('Checking for internet connection')

            ping_address = 'pitt.edu'

            if  self.operating_system == WINDOWS:
                ping_command = f"ping -n 1 {ping_address}"
            else:
                ping_command = f"ping -c 1 {ping_address}"
            
            ping_result = os.system(ping_command)

            if ping_result == 0:
                logging.info('Internet connected')
                self.is_connected = True
            else:
                logging.info('No internet connenction!')
                self.is_connected = False
        except Exception as e:
            logging.error(e)

        return ping_result

    

    def save_system_info(self):

        ## wait for internet conneciton
        while self.check_internet_connection() != 0:
            sleep(5)

        self.get_network_info()


        postgre_connection = None
        try:
            while True:
                try:
                    logging.info('Trying to connect to PSQL Database')
                    ## Password is saved in ~/.pgpass
                    postgre_connection = psql.connect(
                        host=PSQL_DB_HOST,
                        database=DATABASE_NAME,
                        user=DATABASE_USERNAME,
                        passfile=pgpass_conf_location
                    )
                    break
                except Exception as e:
                    logging.error(f"Failed to connect to PSQL DB: {e}")
                    sleep(RECONNECT_INTERVAL)
            
            logging.info("Successfully connected to PSQL DB")

            cur = postgre_connection.cursor()

            mac_addr = self.mac_addr
            hostname = self.hostname
            operating_system_info = self.operating_system_info[:50] ## save at most 50 characters
            processor_model = self.processor_model
            ipv4_addr = self.ipv4_addr
            # internet_connection = self.internet_connection

            ct = datetime.datetime.now()
            logging.info(f"Timestamp: {ct}")

            cur.execute(q1, (mac_addr, ))
            cur.execute(q2, (mac_addr, ))

            cur.execute(q3, (mac_addr, hostname, operating_system_info, processor_model, ct, ipv4_addr))

            from string import ascii_uppercase
            if self.operating_system == WINDOWS:
                for disk in ascii_uppercase:
                    try:
                        total, used, free = shutil.disk_usage(disk+'://')
                        disk_partition = disk
                        total = f"{(total // (BYTES_PER_GIB))} GiB"
                        used = f"{(used // (BYTES_PER_GIB))} GiB"
                        free = f"{(free // (BYTES_PER_GIB))} GiB"
                        cur.execute(q4, (mac_addr, disk_partition, used, free, total))
                        logging.info(f"{disk}: Total-{total}. Used-{used}. Free-{free}")
                    except:
                        pass # doing nothing on exception
            else:
                total, used, free = shutil.disk_usage('/')
                disk_partition = '/'
                total = f"{(total // (BYTES_PER_GIB))} GiB"
                used = f"{(used // (BYTES_PER_GIB))} GiB"
                free = f"{(free // (BYTES_PER_GIB))} GiB"
                cur.execute(q4, (mac_addr, disk_partition, used, free, total))
                logging.info(f"{disk_partition}: Total:{total}. Used:{used}. Free:{free}")
            
            postgre_connection.commit()
        
        finally:
            if postgre_connection:
                postgre_connection.close()






def collect_system_info():
    try:
        sys_info = SystemInfo()

        sys_info.save_system_info()

    except Exception as e:
        logging.error(e)
        
    finally:
        pass
        

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%d-%m-%Y:%H:%M:%S',
                        level=logging.INFO)
    collect_system_info()

