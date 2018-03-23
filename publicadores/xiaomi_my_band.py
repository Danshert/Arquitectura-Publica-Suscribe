#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------
# Archivo: xiaomi_my_band.py
# Capitulo: 3 Patrón Publica-Subscribe
# Autor(es): Perla Velasco & Yonathan Mtz.
# Version: 1.0.1 Mayo 2017
# Descripción:
#
#   Ésta clase define el rol de un publicador, es decir, es un componente que envia mensajes.
#
#   Las características de ésta clase son las siguientes:
#
#                                       xiaomi_my_band.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |  - Enviar mensajes      |  - Simula información  |
#           |      Publicador       |                         |    sobre algunos signos|
#           |                       |                         |    vitales.            |
#           +-----------------------+-------------------------+------------------------+
#
#   A continuación se describen los métodos que se implementaron en ésta clase:
#
#                                             Métodos:
#           +-----------------------------+--------------------------+-----------------------+
#           |         Nombre              |        Parámetros        |        Función        |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Inicializa el      |
#           |       __init__()            |          int: id         |    wearable indicando |
#           |                             |                          |    su identificador.  |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Envía los signos   |
#           |        publish()            |          Ninguno         |    vitales al distri- |
#           |                             |                          |    buidor de mensajes.|
#           +-----------------------------+--------------------------+-----------------------+
#           |   simulate_datetime()       |          Ninguno         |  - Simula valores de  |
#           |                             |                          |    fecha y hora.      |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |          Ninguno         |  - Simula el valor de |
#           |  simulate_x_position()      |                          |    la aceleración en  |
#           |                             |                          |    eje x.             |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Simula el valor de |
#           |  simulate_y_position()      |          Ninguno         |    la aceleración en  |
#           |                             |                          |    eje y.             |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Simula el valor de |
#           |  simulate_z_position()      |          Ninguno         |    la aceleración en  |
#           |                             |                          |    eje z.             |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Simula el valor de |
#           | simulate_body_temperature() |          Ninguno         |    la temperatura     |
#           |                             |                          |    corporal.          |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Simula los pasos   |
#           |    simulate_step_count()    |          Ninguno         |    dados por un       |
#           |                             |                          |    adulto.            |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Simula la bateria  |
#           |  simulate_battery_level()   |          Ninguno         |    restante del       |
#           |                             |                          |    wearable.          |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Simula las horas   |
#           | simulate_hours_of_sleep()   |          Ninguno         |    sueño acumuladas   |
#           |                             |                          |    por un adulto.     |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Simula las calorias|
#           | simulate_calories_burned()  |          Ninguno         |    consumidas por un  |
#           |                             |                          |    adulto en un día.  |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |                          |  - Simula el ritmo    |
#           |    simulate_heart_rate()    |          Ninguno         |    cardiaco del cora- |
#           |                             |                          |    zón.               |
#           +-----------------------------+--------------------------+-----------------------+
#           |                             |          Ninguno         |  - Simula la presión  |
#           | simulate_blood_preasure()   |                          |    arterial.          |
#           +-----------------------------+--------------------------+-----------------------+
#
#-------------------------------------------------------------------------
import pika
import random
import progressbar
from time import sleep
import time


class XiaomiMyBand:
    producer = "Xiaomi"
    model = "Xiaomi My Band 2"
    hardware_version = "2.0.3.2.1"
    software_version = "10.2.3.1"
    step_count = 0
    battery_level = 81
    id = 0

    def __init__(self, id):
        self.id = id

    def publish(self):
        message = {}
        message['body_temperature'] = self.simulate_body_temperature()
        message['id'] = str(self.id)
        message['datetime'] = self.simulate_datetime()
        message['producer'] = self.producer
        message['model'] = self.model
        message['hardware_version'] = self.hardware_version
        message['software_version'] = self.software_version
        # Se establece la conexión con el Distribuidor de Mensajes
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        # Se solicita un canal por el cuál se enviarán los signos vitales
        channel = connection.channel()
        # Se declara una cola para persistir los mensajes enviados
        channel.queue_declare(queue='body_temperature', durable=True)
        print('[x] publicando valor de temperatura...')
        self.draw_progress_bar(2)
        channel.basic_publish(exchange='', routing_key='body_temperature', body=str(message), properties=pika.BasicProperties(
            delivery_mode=2,))  # Se realiza la publicación del mensaje en el Distribuidor de Mensajes
        connection.close()  # Se cierra la conexión
        print('[x] valor publicado!')
        print('')

        sleep(.5)

        message = {}
        message['heart_rate'] = self.simulate_heart_rate()
        message['id'] = str(self.id)
        message['datetime'] = self.simulate_datetime()
        message['producer'] = self.producer
        message['model'] = self.model
        message['hardware_version'] = self.hardware_version
        message['software_version'] = self.software_version
        # Se establece la conexión con el Distribuidor de Mensajes
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        # Se solicita un canal por el cuál se enviarán los signos vitales
        channel = connection.channel()
        channel.queue_declare(queue='heart_rate', durable=True)
        print('[x] publicando valor de ritmo cardiaco...')
        self.draw_progress_bar(2)
        channel.basic_publish(exchange='', routing_key='heart_rate', body=str(message), properties=pika.BasicProperties(
            delivery_mode=2,))  # Se realiza la publicación del mensaje en el Distribuidor de Mensajes
        connection.close()  # Se cierra la conexión
        print('[x] valor publicado!')
        print('')

        sleep(.5)

        message['blood_preasure'] = self.simulate_blood_preasure()
        message['id'] = str(self.id)
        message['datetime'] = self.simulate_datetime()
        message['producer'] = self.producer
        message['model'] = self.model
        message['hardware_version'] = self.hardware_version
        message['software_version'] = self.software_version
        # Se establece la conexión con el Distribuidor de Mensajes
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        # Se solicita un canal por el cuál se enviarán los signos vitales
        channel = connection.channel()
        channel.queue_declare(queue='blood_preasure', durable=True)
        print('[x] publicando valor de presión arterial...')
        self.draw_progress_bar(2)
        channel.basic_publish(exchange='', routing_key='blood_preasure', body=str(message), properties=pika.BasicProperties(
            delivery_mode=2,))  # Se realiza la publicación del mensaje en el Distribuidor de Mensajes
        connection.close()  # Se cierra la conexión
        print('[x] valor publicado!')
        print('')



        sleep(.5)


        message = {}
        message['acelerometro_ejex'] = self.simulate_x_position()
        message['id'] =  str(self.id)
        message['acelerometro_ejey'] = self.simulate_x_position()
        message['acelerometro_ejez'] = self.simulate_x_position()
        message['datetime'] = self.simulate_datetime()
        message['producer'] = self.producer
        message['model'] = self.model
        message['hardware_version'] = self.hardware_version
        message['software_version'] = self.software_version
        # Se establece la conexión con el Distribuidor de Mensajes
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        # Se solicita un canal por el cuál se enviarán los valores del acelerometro
        channel = connection.channel()
        channel.queue_declare(queue='acelerometro_ejex', durable=True)
        print('[x] publicando valores del acelerometro..')
        self.draw_progress_bar(2)
        channel.basic_publish(exchange='', routing_key='acelerometro_ejex', body=str(message), properties=pika.BasicProperties(
            delivery_mode=2,))  # Se realiza la publicación del mensaje en el Distribuidor de Mensajes
        connection.close()  # Se cierra la conexión
        print('[x] valor publicado!')
        print('')

        sleep(.5)

    def simulate_datetime(self):
        return time.strftime("%d:%m:%Y:%H:%M:%S")

    def simulate_x_position(self):
 
        # la posición x óptima de un adulto mayor 
        # debe ser mínimo de 0 y máximo de 10
        return random.uniform(-1, 11)

        

    def simulate_y_position(self):
        return random.uniform(-11, 3)


        # la posición y óptima de un adulto mayor 
        # debe ser mínimo de -10 y máximo de 2
        

    def simulate_z_position(self):
        return random.uniform(-11, 2)
        
        # la posición z óptima de un adulto mayor 
        # debe ser mínimo de -10 y máximo de 1
        

    def simulate_body_temperature(self):
        return random.uniform(67, 72)

    def simulate_step_count(self):
        self.step_count += 1
        return self.step_count

    def simulate_battery_level(self):
        self.battery_level -= 1
        return self.battery_level

    def simulate_hours_of_sleep(self):
        hours_sleep = 10 - random.uniform(0, 3)
        return hours_sleep

    def simulate_calories_burned(self):
        return random.randint(1500, 2500)

    def simulate_heart_rate(self):
        return random.randint(60, 150)

    def simulate_blood_preasure(self):
        return random.randint(100, 200)

    def draw_progress_bar(self, value):
        bar = progressbar.ProgressBar(maxval=value, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()
        for i in xrange(value):
            bar.update(i+1)
            sleep(0.2)
        bar.finish()
