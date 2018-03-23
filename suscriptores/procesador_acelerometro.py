#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: procesador_de_presion.py
# Capitulo: 3 Estilo Publica-Subscribe
# Autor(es): Alejandro Pinedo, Daniel Hernández, Oscar Ulloa, Armando Rodarte
# Version: 1 Marzo 2018
# Descripción:
#
#   Esta clase define el rol de un suscriptor, es decir, es un componente que recibe mensajes.
#
#   Las características de ésta clase son las siguientes:
#
#                                     procesador_acelerometro.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |                         |  - Se suscribe a los   |
#           |                       |                         |    eventos generados   |
#           |                       |  - Procesar valores     |    por el wearable     |
#           |     Procesador de     |    de los ejes:         |    Xiaomi My Band.     |
#           |      Acelerometro     |    "X" , "Y" y "Z" ,    |  - Define el valor ex- |
#           |                       |    para detectar        |    tremo del eje "X"   |
#           |                       |    caidas               |    en minimo = 0 y     |
#           |                       |                         |    maximo = 10, eje "Y"|
#           |                       |                         |    en minimo -10 y     |
#           |                       |                         |    maximo 2, y eje "Z" |
#           |                       |                         |    en minimo -10 y     |
#           |                       |                         |    maximo 1            |
#           |                       |                         |                        |
#           |                       |                         |                        |
#           |                       |                         |                        |
#           |                       |                         |  - Notifica al monitor |
#           |                       |                         |    cuando un valor ex- |
#           |                       |                         |    tremo es detectado. |
#           +-----------------------+-------------------------+------------------------+
#

#
#   A continuación se describen los métodos que se implementaron en ésta clase:
#
#                                               Métodos:
#           +------------------------+--------------------------+-----------------------+
#           |         Nombre         |        Parámetros        |        Función        |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Recibe los signos  |
#           |       consume()        |          Ninguno         |    vitales vitales    |
#           |                        |                          |    desde el distribui-|
#           |                        |                          |    dor de mensajes.   |
#           +------------------------+--------------------------+-----------------------+
#           |                        |  - ch: propio de Rabbit. |  - Procesa y detecta  |
#           |                        |  - method: propio de     |    valores extremos de|
#           |                        |     Rabbit.              |    la presión         |
#           |       callback()       |  - properties: propio de |    arterial.          |
#           |                        |     Rabbit.              |                       |
#           |                        |  - body: mensaje recibi- |                       |
#           |                        |     do.                  |                       |
#           +------------------------+--------------------------+-----------------------+
#           |    string_to_json()    |  - string: texto a con-  |  - Convierte un string|
#           |                        |     vertir en JSON.      |    en un objeto JSON. |
#           +------------------------+--------------------------+-----------------------+
#
#
#           Nota: "propio de Rabbit" implica que se utilizan de manera interna para realizar
#            de manera correcta la recepcion de datos, para éste ejemplo no shubo necesidad
#            de utilizarlos y para evitar la sobrecarga de información se han omitido sus
#            detalles. Para más información acerca del funcionamiento interno de RabbitMQ
#            puedes visitar: https://www.rabbitmq.com/
#
#-------------------------------------------------------------------------
import pika
import sys
sys.path.append('../')
from monitor import Monitor
import time


class ProcesadorAcelerometro:

    def consume(self):
        try:
            # Se establece la conexión con el Distribuidor de Mensajes
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            # Se solicita un canal por el cuál se enviarán los signos vitales
            channel = connection.channel()
            # Se declara una cola para leer los mensajes enviados por el
            # Publicador
            channel.queue_declare(queue='acelerometro_ejex', durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(self.callback, queue='acelerometro_ejex')
            channel.start_consuming()  # Se realiza la suscripción en el Distribuidor de Mensajes
        except (KeyboardInterrupt, SystemExit):
            channel.close()  # Se cierra la conexión
            sys.exit("Conexión finalizada...")
            time.sleep(1)
            sys.exit("Programa terminado...")

    def callback(self, ch, method, properties, body):
        json_message = self.string_to_json(body)
        
        if float(json_message['acelerometro_ejex']) < 0 or float(json_message['acelerometro_ejex']) > 10:
            monitor = Monitor()
            monitor.print_notification('se detecto una caida',json_message['datetime'], json_message['id'])
        
        elif float(json_message['acelerometro_ejey']) < -10 or float(json_message['acelerometro_ejey']) > 2:
            monitor = Monitor()
            monitor.print_notification('se detecto una caida',json_message['datetime'], json_message['id'])

        elif float(json_message['acelerometro_ejez']) < -10 or float(json_message['acelerometro_ejez']) > 1:
            monitor = Monitor()
            monitor.print_notification('se detecto una caida',json_message['datetime'], json_message['id'])
         


        time.sleep(1)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def string_to_json(self, string):
        message = {}
        string = string.replace('{', '')
        string = string.replace('}', '')
        values = string.split(', ')
        for x in values:
            v = x.split(': ')
            message[v[0].replace('\'', '')] = v[1].replace('\'', '')
        return message

if __name__ == '__main__':
    p_acelerometro = ProcesadorAcelerometro()
    p_acelerometro.consume()
