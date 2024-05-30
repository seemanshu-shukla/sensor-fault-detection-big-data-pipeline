import argparse

from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry.json_schema import JSONDeserializer
from src.entity.generic import Generic
from src.kafka_config import sasl_conf
from src.database.mongodb import MongodbOperation




def consumer_using_sample_file(topic,file_path):
    schema_str = Generic.get_schema_to_produce_consume_data(file_path=file_path)
    json_deserializer = JSONDeserializer(schema_str, #Please note that here we are just defining the JSONDeserializer.
                                         from_dict=Generic.dict_to_object)  #The JSONDeserializer will give us dict() and by mentioning from_dict we are converting dict() into object

    consumer_conf = sasl_conf()
    consumer_conf.update({
        'group.id': 'group1',   #We are setting the group id that will help kafka to identify from where to consume data. This is just a tracker that helps Kafka to have a track to whom it is sending data and how much data it has send to that group. Here we have a mongodb source that is consuming the data that's why we have made only one group. But incase there any more than one consumers then we can define multiple groups as well. In order to uniquely identify multiple receivers/consumers we need to define unique group names for each
        'auto.offset.reset': "earliest"}) #Offset means row number. reset to earliest means move the row to the earliest one

    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])

    mongodb = MongodbOperation()
    records = [] #So this is the list that will be used to append the records that we want to store in mongodb. We will be using insert many functionality which will be triggered once len(record)==5000.
    x = 0
    while True:  #Denoting that infinite time we are going to consume the data
        try:
            # SIGINT can't be handled when polling, limit timeout to 1 second.
            msg = consumer.poll(1.0)  #poll we can see as a way to starting the process
            if msg is None:
                continue

            record: Generic = json_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE)) #Here, we are calling the jasondeserializer that we defined above. In this single step we are deserializing which gives dict() followed by converting this dict() into mongodb
            #So, to conclude json_deserializer() will be giving an object(of a record in kafka's topic) which we are appending in record list which is of Generic (class in generic.py) type

            # mongodb.insert(collection_name="car",record=car.record)

            if record is not None:
                records.append(record.to_dict())  ## record is of Generic class type hence we are calling a method defined in that class .to_dict(). We did this since to store data in mongodb we need to have data in dict() type
                if x % 5000 == 0:
                    mongodb.insert_many(collection_name="car", records=records)
                    records = []
            x = x + 1
        except KeyboardInterrupt:
            break

    consumer.close()
