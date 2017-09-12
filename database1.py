import sqlite3
import os

DATABASE = 'database.db'


def parse_message(str):
    index = 0
    count = []
    while index >= 0:
        index = str.find(',')
        if index >= 0:
            TIME = str[0:(index)]
            str = str[index+1:]
            count.append(TIME)
    return count

def updateDataBase(db, str, balloonID):
    msg = parse_message(str)
    ##time = msg[0]
    ##temp = msg[1]
    ##humidty = msg[2]
    ##pressure = msg[3]
    ##pitch = msg[4]
    ##roll = msg[5]
    ##yaw = msg[6]
    ##mag_x = msg[7]
    ##mag_y = msg[8]
    ##mag_z = msg[9]
    ##acc_x = msg[10]
    ##acc_y = msg[11]
    ##acc_z = msg[12]
    ##gyro_x = msg[13]
    ##gyro_y = msg[14]
    ##gyro_z = msg[15]
    db.execute('insert into BalloonTicket (time_stamp, balloon_id, temperature, humidity, pressure, pitch, roll, yaw, magnitude_x, magnitude_y, magnitude_z, acceleration_x, acceleration_y, acceleration_z, gyroscope_x, gyroscope_y, gyroscope_z)  '
               'VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(msg[0], balloonID, msg[1],msg[2],msg[3],msg[4],msg[5],msg[6],msg[7],msg[8],msg[9],msg[10],msg[11],msg[12],msg[13],msg[14],msg[15]))
    print(msg)
    return

def createDB():
    db = sqlite3.connect(DATABASE)
    db.execute('create table ServerNormalization (time_stamp text, temperature double, humidity double, pressure double, pitch double, roll double, yaw double, magnitude_x double, magnitude_y double, magnitude_z double, acceleration_x double, acceleration_y double, acceleration_z double, gyroscope_x double, gyroscope_y double, gyroscope_z double)')
    db.execute('create table BalloonTicket (time_stamp text, balloon_id int, temperature double, humidity double, pressure double, pitch double, roll double, yaw double, magnitude_x double, magnitude_y double, magnitude_z double, acceleration_x double, acceleration_y double, acceleration_z double, gyroscope_x double, gyroscope_y double, gyroscope_z double)')
    db.commit()
    return db

def openDB():
    return sqlite3.connect(DATABASE)

def dbopen():
    if os.path.isfile(DATABASE):
        print('DB Exists')
        return openDB()
    else:
        return createDB()


db = dbopen()
updateDataBase(db, '5/26/2017 13:19:57,24.1283989,56.79413605,990.657959,9.463278321,259.9766744,322.4402228,-12.60565567,-36.66516876,2.529813766,0.385246575,0.166312903,0.927997649,-0.104043715,0.045720126,-0.015003573,', 0)
db.commit()
db.close()