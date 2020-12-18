import dht
import network
import ntptime
import ujson
import utime

from machine import RTC
from machine import Pin
from time import sleep
from third_party import rd_jwt

from umqtt.simple import MQTTClient


# Konstanta-konstanta aplikasi

# WiFi AP Information
AP_SSID = "Samsung J6"
AP_PASSWORD = "87654321"

# Decoded Private Key
PRIVATE_KEY = (25227293408750212103803984621973022368337087791194819290106961179505928471356027894862664595938283787358179394966125920037042094782213079643328685815887096494006382310124523500502139414809827487508080764378614107681559276426758202274221975698900638421514119434237682290562016441424895376719431734047549512941246198638142048447254518916856430490508073275745724361507595943091087256308492232400470006591937489990944153801923383430048950834367437523175560819364642056776125600129415088989655129004645476545222245447218571872739749027405356639845080147278573885316359132034311256969711550421731594088951732951967945289843, 65537, 25059463023987176071070436591163247161162591395617344867864767684621136906079752994239198130219238183633746384358297809181553586713106393302414525768650775422376817595730909324598162534805294402616286461721045470866490539003286475216352973739629987058897885000660807708590228914249997923612794685723019375955069087312095470333138497715092741302643286901737765013015812012069635263144783315801946815939411548164462143681297525203755571945864364946801100460832289498339705469972916512145655297793737284280265275423740456360331769392045069669304847462910704828126564722079499933366842863264008146364938455697972043067577, 166979330482275512285102184315645933613053876305287104163051361772327197161418371412594984159880237462461346245512558048951207641855747541787578531122686264392165313431021612257467063584861738708559963517327833894684188232149277346946640701993666656793549911650472631913288090230428012818366254719793659329317, 151080336325986369127145112227225828898013306151733463884885408110857166092901664436175532774122433830546439291081630602545510221956508255784631788225584970849893569050200216160310348464465687424598790502022067934783365734558736227243045700537839405894421450750128127013954362485687663107746634419053231191479)


#Project ID of IoT Core
PROJECT_ID = "hsc2020-01"
# Location of server
REGION_ID = "asia-east1"
# ID of IoT registry
REGISTRY_ID = "latihan_iot_esp"
# ID of this device
DEVICE_ID = "esp32"

# MQTT Information
MQTT_BRIDGE_HOSTNAME = "mqtt.googleapis.com"
MQTT_BRIDGE_PORT = 8883


dht22_obj = dht.DHT22(Pin(4))
led_obj = Pin(23, Pin.OUT)
def suhu_kelembaban():
    # Read temperature from DHT 22
    #
    # Return
    #    * List (temperature, humidity)
    #    * None if failed to read from sensor
    while True:
        try:
            dht22_obj.measure()
            return dht22_obj.temperature(),dht22_obj.humidity()
            sleep(3)
            break
        except:
            return None
def connect():
    # Connect to WiFi
    print("Connecting to WiFi...")
    
    # Activate WiFi Radio
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # If not connected, try tp connect
    if not wlan.isconnected():
        # Connect to AP_SSID using AP_PASSWORD
        wlan.connect(AP_SSID, AP_PASSWORD)
        # Loop until connected
        while not wlan.isconnected():
            pass
    
    # Connected
    print("  Connected:", wlan.ifconfig())


def set_time():
    # Update machine with NTP server
    print("Updating machine time...")

    # Loop until connected to NTP Server
    while True:
        try:
            # Connect to NTP server and set machine time
            ntptime.settime()
            # Success, break out off loop
            break
        except OSError as err:
            # Fail to connect to NTP Server
            print("  Fail to connect to NTP server, retrying (Error: {})....".format(err))
            # Wait before reattempting. Note: Better approach exponential instead of fix wiat time
            utime.sleep(0.5)
    
    # Succeeded in updating machine time
    print("  Time set to:", RTC().datetime())


def on_message(topic, message):
    print((topic,message))


def get_client(jwt):
    #Create our MQTT client.
    #
    # The client_id is a unique string that identifies this device.
    # For Google Cloud IoT Core, it must be in the format below.
    #
    client_id = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(PROJECT_ID, REGION_ID, REGISTRY_ID, DEVICE_ID)
    client = MQTTClient(client_id.encode('utf-8'),
                        server=MQTT_BRIDGE_HOSTNAME,
                        port=MQTT_BRIDGE_PORT,
                        user=b'ignored',
                        password=jwt.encode('utf-8'),
                        ssl=True)
    client.set_callback(on_message)

    try:
        client.connect()
    except Exception as err:
        print(err)
        raise(err)

    return client


def publish(client, payload):
    # Publish an event
    
    # Where to send
    mqtt_topic = '/devices/{}/{}'.format(DEVICE_ID, 'events')
    
    # What to send
    payload = ujson.dumps(payload).encode('utf-8')
    
    # Send    
    client.publish(mqtt_topic.encode('utf-8'),
                   payload,
                   qos=1)
    
    
def subscribe_command():
    print("Sending command to device")
    client_id = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(PROJECT_ID, REGION_ID, REGISTRY_ID, DEVICE_ID)
    command = 'baca'
    data = command.encode("utf-8")
    while True:
        dht22_obj.measure()
        temp = dht22_obj.temperature()
        humi = dht22_obj.humidity()
        print("Suhu: ", temp)
        print("Kelembaban: ", humi)
        sleep(3)

def subscribe_command1():
    print("Sending command to device")
    client_id = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(PROJECT_ID, REGION_ID, REGISTRY_ID, DEVICE_ID)
    command = 'PING!'
    data = command.encode("utf-8")
    while True:
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        led_obj.value(0)
        sleep(.5)
        led_obj.value(1)
        sleep(.5)
        break
def subscribe_command2():
    print("Sending command to device")
    client_id = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(PROJECT_ID, REGION_ID, REGISTRY_ID, DEVICE_ID)
    #ukur = f"/devices/{DEVICE_ID}/commands/#"
    command = 'Baca Suhu'
    data = command.encode("utf-8")
    while True:
        dht22_obj.measure()
        temp = dht22_obj.temperature()
        print(temp)
        sleep(3)
    publish(client, temp)
def subscribe_command3():
    print("Sending command to device")
    client_id = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(PROJECT_ID, REGION_ID, REGISTRY_ID, DEVICE_ID)
    #ukur = f"/devices/{DEVICE_ID}/commands/#"
    command = 'Baca Kelembaban'
    data = command.encode("utf-8")
    while True:
        dht22_obj.measure()
        humi = dht22_obj.humidity()
        print(humi)
        sleep(3)
    publish(client, humi)
# Connect to Wifi
connect()
# Set machine time to now
set_time()

# Create JWT Token
print("Creating JWT token.")
start_time = utime.time()
jwt = rd_jwt.create_jwt(PRIVATE_KEY, PROJECT_ID)
end_time = utime.time()
print("  Created token in", end_time - start_time, "seconds.")

# Connect to MQTT Server
print("Connecting to MQTT broker...")
start_time = utime.time()
client = get_client(jwt)
end_time = utime.time()
print("  Connected in", end_time - start_time, "seconds.")

# Read from DHT22
print("Reading from DHT22")
result1 = suhu_kelembaban()
print("Suhu dan Kelembaban ", result1)

# Publish a message

print("Publishing message...")
if result1 == None:
   result1 = "Fail to read sensor...."


publish(client, result1)

# Need to wait because command not blocking
utime.sleep(1)

# Disconnect from client
client.disconnect()
#publish_events()
#publish_state()
#subscribe_config()
#subscribe_command()
#subscribe_command1()
#subscribe_command2()
#subscribe_command3()
