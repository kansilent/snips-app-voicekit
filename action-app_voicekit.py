#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import grove.grove_relay
# import grove.grove_temperature_humidity_sensor_sht3x
from gpiozero import LED

CONFIG_INI = "config.ini"

# If this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
# Hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

class VoiceKit(object):
    """Class used to wrap action code with mqtt connection
        
        Please change the name refering to your application
    """

    def __init__(self):
        # get the configuration if needed
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
            self.mqtt_address = self.config.get("secret").get("mqtt").encode()
        except :
            self.config = None
            self.mqtt_address = MQTT_ADDR

        self.relay = grove.grove_relay.Grove(12)
        # self.temperature_humidity_sensor = grove.grove_temperature_humidity_sensor_sht3x.Grove()
        # self.led = LED(12)

        # start listening to MQTT
        self.start_blocking()
        self.previous_intent = "nothing"
        
    def good_morning(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")
        
        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        # self.led.on()
        self.relay.on()

        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, "Good morning, the morning pills are 1 piece A and 2 pieces B", "")

    def thank_you1(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")
        
        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        # self.led.off()
        self.relay.off()

        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, "No problem, you are super xin xin", "")
        
    def good_afternoon(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")
        
        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        # self.led.on()
        self.relay.on()

        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, "Good afternoon, the afternoon pills are 2 pieces C", "")

    def thank_you2(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")
        
        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        # self.led.off()
        self.relay.off()

        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, "You are welcome, you are so sweet xin xin", "")
        
    def good_evening(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")
        
        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        # self.led.on()
        self.relay.on()

        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, "Good evening, the evening pills are 2 pieces A", "")

    def thank_you3(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")
        
        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        # self.led.off()
        self.relay.off()

        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, "It's my pleasure, good night xin xin", "")
    
    
    def thank_you(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")
        
        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        # self.led.off()
        self.relay.off()

        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, "ha ha ha ha ha", "")

    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name

        if coming_intent == 'Winnie:Morning_Pill_reminder':
            self.previous_intent = coming_intent
            self.good_morning(hermes, intent_message)   
        elif coming_intent == 'Winnie:Afternoon_Pill_reminder':
            self.previous_intent = coming_intent
            self.good_afternoon(hermes, intent_message)
        elif coming_intent == 'Winnie:Evening_Pill_reminder':
            self.previous_intent = coming_intent
            self.good_evening(hermes, intent_message)
        elif coming_intent == 'Winnie:compliments':
            if self.previous_intent == "Winnie:Morning_Pill_reminder":
                self.thank_you1(hermes, intent_message)
            elif self.previous_intent == "Winnie:Afternoon_Pill_reminder":
                self.thank_you2(hermes, intent_message)
            elif self.previous_intent == "Winnie:Evening_Pill_reminder":
                self.thank_you3(hermes, intent_message)   
            else:
                self.thank_you(hermes, intent_message)

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(self.mqtt_address) as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    VoiceKit()
