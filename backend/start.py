# Imports
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
from RPi import GPIO
from ds1820 import Ds1820
from mcp3008 import Mcp3008
from DP1Database import Database
from i2c_lcd_driver import I2c_led_driver

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

conn = Database(app=app, user='yourusername', password='youruserpassword', db='smartterradb')
endpoint = '/api/v1'
mcp = Mcp3008()
lcd = I2c_led_driver()

heatlamp = 20
uvlamp = 16
deurcontact = 21
GPIO.setmode(GPIO.BCM)
control_pins = [12, 25, 24, 23]
for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

GPIO.setup(heatlamp, GPIO.OUT)
GPIO.setup(uvlamp, GPIO.OUT)
GPIO.setup(deurcontact, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

statusVorige = 1

@socketio.on('clickonbutton')
def geklikt(data):
    print(data)
    data = (data["drukknop"])
    if 'Geef beloning' in data:
        halfstep_seq = [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1]
        ]

        terugkeren_seq = [
            [0, 0, 0, 1],
            [0, 0, 1, 1],
            [0, 0, 1, 0],
            [0, 1, 1, 0],
            [0, 1, 0, 0],
            [1, 1, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 1]
        ]
        for i in range(100):
            for terugkeren in range(8):
                for pin in range(4):
                    GPIO.output(control_pins[pin], terugkeren_seq[terugkeren][pin])
                time.sleep(0.001)
        time.sleep(1)
        for i in range(100):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
                time.sleep(0.001)
        conn.set_data("insert into acties (idhardware, tijdstip, beschrijving) values ('VL', now() , 'Manueel')")
        gegevens = conn.get_data(
            "SELECT count(idhardware) as beloningen from acties  where idhardware = 'VL'  and day(tijdstip) = day(now())")
        print("hh")
        print(gegevens)
        socketio.emit('voederluik', (gegevens))

    if 'WARMTE' in data:
        status = GPIO.input(heatlamp)
        if (status == 0):
            GPIO.output(heatlamp, 1)

            socketio.emit(('lighttempoff'))
        else:
            GPIO.output(heatlamp, 0)
            conn.set_data("insert into acties (idhardware, tijdstip, beschrijving) values ('L1', now() , 'Manueel')")
            socketio.emit(('lighttempon'))

    if 'UV' in data:
        status = GPIO.input(uvlamp)
        if (status == 0):
            GPIO.output(uvlamp, 1)
            socketio.emit(('lightuvoff'))

        else:
            GPIO.output(uvlamp, 0)
            print('insert into ')
            conn.set_data("insert into acties (idhardware, tijdstip, beschrijving) values ('L2', now() , 'Manueel')")

            socketio.emit(('lightuvon'))

@app.route(endpoint + '/sensordata', methods=['GET'])
def sensordata():
    if request.method == 'GET':
        tempR = Ds1820('/sys/bus/w1/devices/28-0113170f67f8/w1_slave')
        tempL = Ds1820('/sys/bus/w1/devices/28-011316e13b64/w1_slave')
        tempSteen = Ds1820('/sys/bus/w1/devices/28-011316e13b64/w1_slave')

        tempR = tempR.temperature()
        tempL = tempL.temperature()
        tempSteen = tempSteen.temperature()

        tempR = round(tempR)
        tempL = round(tempL)
        tempSteen = round(tempSteen)

        statusdeur = GPIO.input(deurcontact)
        data = {"Links": tempL, "Rechts": tempR, "Steen": tempSteen, "statusdeur": statusdeur}

        return jsonify(data)

@socketio.on('deurtoestand')
def geopend():
    conn.set_data("insert into acties (idhardware, tijdstip, beschrijving) values ('D1', now() , 'Manueel')")

def lcdklasse():
    tempR = Ds1820('/sys/bus/w1/devices/28-0113170f67f8/w1_slave')
    tempL = Ds1820('/sys/bus/w1/devices/28-011316e13b64/w1_slave')
    tempSteen = Ds1820('/sys/bus/w1/devices/28-011316e13b64/w1_slave')

    tempR = tempR.temperature()
    tempL = tempL.temperature()
    tempSteen = tempSteen.temperature()

    gemiddelde = (tempR + tempL + tempSteen) / 3
    gemiddelde = round(gemiddelde)
    lcd.main(gemiddelde)

def logsensoren():
    lcdklasse()
    tempR = Ds1820('/sys/bus/w1/devices/28-0113170f67f8/w1_slave')
    tempL = Ds1820('/sys/bus/w1/devices/28-011316e13b64/w1_slave')
    tempSteen = Ds1820('/sys/bus/w1/devices/28-011316e13b64/w1_slave')
    tempR = tempR.temperature()
    tempL = tempL.temperature()
    tempSteen = tempSteen.temperature()
    uvwaarde = mcp.read_channel(0)

    conn.set_data("insert into sensor_histogram (idhardware, tijdstip, waarde) values ('S1', now() , %s)" % tempL)
    conn.set_data(
        "insert into sensor_histogram (idhardware, tijdstip, waarde) values ('S2', now() , %s)" % tempSteen)
    conn.set_data("insert into sensor_histogram (idhardware, tijdstip, waarde) values ('S3', now() , %s)" % tempR)
    conn.set_data(
        "insert into sensor_histogram (idhardware, tijdstip, waarde) values ('S4', now() , %s)" % uvwaarde)

@socketio.on('connect')
def connect():
    status = GPIO.input(heatlamp)
    if (status == 1):
        socketio.emit(('lighttempoff'))
    elif (status == 0):
        socketio.emit(('lighttempon'))
    status2 = GPIO.input(uvlamp)
    if (status2 == 1):
        socketio.emit(('lightuvoff'))
    elif (status2 == 0):
        socketio.emit(('lightuvon'))

    data = conn.get_data(
        "select V.dag, H.beschrijving from voedselschema as V join hardware as H where V.idhardware = H.idhardware")
    socketio.emit('tabelaanpassen', (data))
    lcdklasse()
    logsensoren()
    gegevens = conn.get_data(
        "SELECT count(idhardware) as beloningen from acties  where idhardware = 'VL'  and day(tijdstip) = day(now())")
    socketio.emit('voederluik', (gegevens))

@socketio.on('aanpassen')
def aanpassen(data):
    if (data['dag'] == 0):
        dag = 'Maandag'
    if (data['dag'] == 1):
        dag = 'Dinsdag'
    if (data['dag'] == 2):
        dag = 'Woensdag'

    if (data['dag'] == 3):
        dag = 'Donderdag'
    if (data['dag'] == 4):
        dag = 'Vrijdag'
    if (data['dag'] == 5):
        dag = 'Zaterdag'
    if (data['dag'] == 6):
        dag = 'Zondag'

    if (data['gekozen'] == 'Groente'):
        beschrijving = 'V1'
    if (data['gekozen'] == 'Korrel'):
        beschrijving = 'V2'
    if (data['gekozen'] == 'Krekel'):
        beschrijving = 'V3'
    if (data['gekozen'] == 'Sprinkhaan'):
        beschrijving = 'V4'
    if (data['gekozen'] == 'Meelworm'):
        beschrijving = 'V5'

    conn.set_data("update voedselschema set idhardware =  ('%s') where dag = '%s' " % (beschrijving, dag))

    data = conn.get_data(
        "select V.dag, H.beschrijving from voedselschema as V join hardware as H where V.idhardware = H.idhardware")
    socketio.emit('tabelaanpassen', (data))

# Start app
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
