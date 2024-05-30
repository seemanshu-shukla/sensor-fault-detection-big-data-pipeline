
import pandas as pd
import json

class Generic:

    def __init__(self, record: dict):
        for k, v in record.items():
            setattr(self, k, v)

    @staticmethod
    def dict_to_object(data: dict, ctx):
        print(data, ctx)
        return Generic(record=data)


    def to_dict(self):
        return self.__dict__

    @classmethod
    def get_object(cls, file_path):  #This will take the csv file having IOT reading and will give each records
        chunk_df = pd.read_csv(file_path, chunksize=10)
        n_row = 0
        for df in chunk_df:
            for data in df.values:
                generic = Generic(dict(zip(df.columns, list(map(str,data))))) #Please note this generic is baically an object or an instance of our class Generic
                # cars.append(car)
                # print(n_row)
                n_row += 1
                yield generic

    @classmethod
    def export_schema_to_create_confluent_schema(cls, file_path):
        columns = next(pd.read_csv(file_path, chunksize=10)).columns

        schema = dict()
        schema.update({
                    "type": "record",
                    "namespace": "com.mycorp.mynamespace",
                    "name": "sampleRecord",
                    "doc": "Sample schema to help you get started.",
                    })

        fields = []    
        for column in columns:
            fields.append(
                        {
                        "name": f"{column}",
                        "type": "string",
                        "doc": "The string type."  
                        }
            )

        schema.update({"fields":fields})


    
        json.dump(schema,open("schema.json","w"))
        schema = json.dumps(schema)

        print(schema)
        return schema
        

    @classmethod
    def get_schema_to_produce_consume_data(cls, file_path):  #This will take data produced from IOT devices(sample_data) and convert it into json format schema representing schema of topics
        columns = next(pd.read_csv(file_path, chunksize=10)).columns #We cannot read datafile having size more than our RAM. So that's we here we are reading in chunks(10 rows in each chunk). Now no matter how big datafile is we will be able to read it

        schema = dict()
        schema.update({
            "$id": "http://example.com/myURI.schema.json",
            "$schema": "http://json-schema.org/draft-07/schema#",
            "additionalProperties": False,
            "description": "Sample schema to help you get started.",
            "properties": dict(),
            "title": "SampleRecord",
            "type": "object"})
        for column in columns:
            schema["properties"].update(
                {
                    f"{column}": {
                        "description": f"generic {column} ",
                        "type": "string"   #Note an entry can be int string float anothing. Just for simplification we have decided to represent all the datapoints as str
                    }
                }
            )
        
    
        schema = json.dumps(schema) #Convert the defined dict() for into target json schema

        print(schema)
        return schema
        

    def __str__(self):
        return f"{self.__dict__}"


def instance_to_dict(instance: Generic, ctx):
    return instance.to_dict() #Select .to_dict and click f12 and also see equivalent breakdown in jupyter notebook
