#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Confluent Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# A simple example demonstrating use of JSONSerializer.

import argparse
from uuid import uuid4
from src.kafka_config import sasl_conf, schema_config
from six.moves import input
from src.kafka_logger import logging
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
import pandas as pd
from typing import List
from src.entity.generic import Generic, instance_to_dict

def car_to_dict(car: Generic, ctx):
    """
    Returns a dict representation of a User instance for serialization.
    Args:
        user (User): User instance.
        ctx (SerializationContext): Metadata pertaining to the serialization
            operation.
    Returns:
        dict: Dict populated with user attributes to be serialized.
        :param car:
    """

    # User._address must not be serialized; omit from dict
    return car.record


def delivery_report(err, msg):
    """
    Reports the success or failure of a message delivery.
    Args:
        err (KafkaError): The error that occurred on None on success.
        msg (Message): The message that was produced or failed.
    """

    if err is not None:
        logging.info("Delivery failed for Sensor record {}: {}".format(msg.key(), err))
        return
    logging.info('User record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))


def product_data_using_file(topic,file_path):
    logging.info(f"Topic: {topic} file_path:{file_path}")
    schema_str = Generic.get_schema_to_produce_consume_data(file_path=file_path)
    schema_registry_conf = schema_config()
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    string_serializer = StringSerializer('utf_8') #In python everything is object. Before storing them into disk we need to serialize them. Like in ML we make model which are objects and to store them on disk we store them in pickel format which is a serialized file.
    json_serializer = JSONSerializer(schema_str, schema_registry_client, instance_to_dict) #This is used to serialize the json format so that we can store it in the disk(publish to kafka). Select instance_to_dict and press f12. See JSONSerializer() breakdown in Jupyter notebook.
    producer = Producer(sasl_conf()) #Connect to Kafka server

    print("Producing user records to topic {}. ^C to exit.".format(topic))
    # while True:
    # Serve on_delivery callbacks from previous calls to produce()
    producer.poll(0.0) #.poll() ensures that whenever we are sending data it is published successfully
    try:
        #In below we are converting the data read from csv into object and then we perform serialization(object to dict()) and publish it to kafka. Also as soon as a record is read we are sending it to kafka and are not waiting for all the records in a chunk to get read first.
        for instance in Generic.get_object(file_path=file_path): #Explore .get_object()
            print(instance)
            logging.info(f"Topic: {topic} file_path:{instance.to_dict()}")
            producer.produce(topic=topic,
                             key=string_serializer(str(uuid4()), instance.to_dict()),
                             value=json_serializer(instance, SerializationContext(topic, MessageField.VALUE)),
                             on_delivery=delivery_report) #delivery_report is a function which we have defined to capture successfully and failed publish to kafka
            print("\nFlushing records...")
            producer.flush()
    except KeyboardInterrupt:
        pass
    except ValueError:
        print("Invalid input, discarding record...")
        pass

    
