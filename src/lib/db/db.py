#!/usr/bin/env python

import sqlite3,os,re

from lib.db import db 
from lib.db import user 
from subprocess import call

import lib.logging.logger as logger

def file_exists(_file):
    return os.path.exists(_file)

def write_to_db(location_bool, coordinates, ip_addr): 
    if location_bool is None or coordinates is None or ip_addr is None:
        return
    elif not re.search("true|false|NULL", location_bool, re.I|re.M):
        logger.log("ERROR", str(location_bool) + " is not a known mode.")
    elif not re.search("\A\((\d|\-\d)+\.\d+,\s(\d|\-\d)+\.\d+\)|NULL", coordinates, re.M | re.I): 
        logger.log("ERROR", "Improper coordinate format -> " + str(coordinates) + ".")
    elif not re.search("\A\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$|NULL", ip_addr, re.M|re.I):
        logger.log("ERROR", "Improper ip address format -> " + str(ip_addr) + ".") 
    else:
        coor = re.sub("[\(\)]", "", str(coordinates))
        db.execute("insert into connected (location_bool, coordinates, ip_addr) values(\"" + str(location_bool) + "\", \"" + str(coor) + "\", \"" + str(ip_addr) + "\")")
        db.commit()

def read_from_db(column):
    query = db.execute("select * from connected")
    for row in query:
        if column == 'location_bool' and row[1] is not None:
            return str(row[1])
        elif column == 'coordinates' and row[2] is not None:
            return str(row[2])
        elif column == 'ip_addr' and row[3] is not None:
            return str(row[3])
        else:
            logger.log("ERROR", "Not a known column or DB is empty.") 
            return

def update_db(column,value):
    if column is None or value is None:
        return
    try:
        if read_from_db('location_bool') is None or read_from_db('coordinates') is None or read_from_db('ip_addr') is None:
            logger.log("ERROR", "You must write to the database first before updating!")
            return
        elif re.search("true|false", value, re.I|re.M) and column == 'location_bool':
            db.execute("update connected set location_bool = \"" + value + "\"")
            db.commit()
        elif re.search("\A(\d|\-\d)+\.\d+,\s(\d|\-\d)+\.\d+", value, re.M | re.I) and column == 'coordinates':    
            db.execute("update connected set coordinates = \"" + value + "\"")
            db.commit()
        elif re.search("\A\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$", value, re.M|re.I) and column == 'ip_addr':
            db.execute("update connected set ip_addr = \"" + value + "\"")
            db.commit()
        else:
            logger.log("ERROR", str(column) + " is not a known column for the connected table in the imagecapture db.")
            return
    except sqlite3.OperationalError:
      logger.log("ERROR", "The database is lock, could not add coordinates to DB.")

def add_location_to_db(location_bool):
    try:
        if read_from_db('location_bool') is None:
            write_to_db(location_bool,'NULL','NULL')
            logger.log("INFO", "Writing location_bool to DB.")
        elif read_from_db('location_bool') != location_bool and read_from_db('location_bool') is not None:
            update_db('location_bool', location_bool)
            logger.log("INFO", "Updating location_bool variable in DB.")
        else:
            return
    except sqlite3.OperationalError:
        call(['/usr/bin/rm', '/home/' + user.name() + '/.imagecapture/imagecapture.db'])
        logger.log("ERROR", "The database is locked, could not add location_bool to DB.")
        pass

def add_coordinates_to_db(coordinates):
    try:
        if read_from_db('coordinates') is None:
            write_to_db('NULL', coordinates,'NULL')
            logger.log("INFO", "Writing coordinates to DB.")
        elif not read_from_db('coordinates') == coordinates and read_from_db('coordinates') is not None:
            update_db('coordinates', ip_addr)
            logger.log("INFO", "Updating coordinates variable in DB.")
        else:
            return
    except sqlite3.OperationalError:
        call(['/usr/bin/rm', '/home/' + user.name() + '/.imagecapture/imagecapture.db'])
        logger.log("ERROR", "The database is locked, could not add coordinates to DB.")
        pass

def add_ip_to_db(ip_addr):
    try:
        if read_from_db('ip_addr') is None:
            write_to_db('NULL','NULL', ip_addr)
            logger.log("INFO", "Writing ip_addr to DB.")
        elif read_from_db('ip_addr') != ip_addr and read_from_db('ip_addr') is not None:
            update_db('ip_addr', ip_addr)
            logger.log("INFO", "Updating ip_addr variable in DB.")
        else:
            return
    except sqlite3.OperationalError:
        call(['/usr/bin/rm', '/home/' + user.name() + '/.imagecapture/imagecapture.db'])
        logger.log("ERROR", "The database is locked, could not add IP address to DB.")
        pass
