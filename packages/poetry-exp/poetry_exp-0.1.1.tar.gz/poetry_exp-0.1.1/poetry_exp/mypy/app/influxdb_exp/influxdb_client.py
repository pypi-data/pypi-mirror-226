import argparse

from influxdb import InfluxDBClient
import datetime
import time


def create_influxClient():
    host = '127.0.0.1'
    port = '8086'
    user = ''
    password = ''
    dbname = ''
    use_ssl = True
    return InfluxDBClient(host, port, user, password, dbname, use_ssl)


def read_data_points(client, tags, measurement):
    result_set =  client.query('select * from ' + measurement + ' ORDER BY time DESC;')
    #result_set =  client.query('select * from ' + measurement)
    #self.log.info("result_set: {0}".format(result_set))
    data_points =  result_set.get_points(tags=tags)
    #data_points =  result_set.get_points()
    print(data_points)
    for data_point in data_points:
        print (data_point)

def delete_data_points(client, measurement):
    delete_result =  client.query('delete from ' + measurement)
    print("Delete result: {0}".format(delete_result))

def execute_query(client, query):
    result = client.query(query)
    print("Result: {0}".format(result))

def write_points(client, json_body):
   result = client.write_points(json_body)
   print("Write Result: {0}".format(result))


if __name__ == '__main__':
   client = create_influxClient()
   #delete_data_points(client, "stream1")
   #delete_data_points(client, "classifier_results")
   #read_data_points(client, {}, "cam_serial2_classifier_results")
   #read_data_points(client, {}, "stream1")
   execute_query(client, "show measurements")

   #insert_query = "insert classifier_results2   Height=2,Width=3"
   #execute_query(client, insert_query)
   #print (datapoints)

   #read_data_points(client, {}, "classifier_results")

	 
   

   
   exit(0)
   #delete_data_points(client, "camera")
   cam1 = [
           {
            "measurement": "camera",
            "fields": {
                "ImageStore": "1",
                "Cam_Sn":"cam1",
                "Channels":3.0,
                "Height":1200.0,
                "ImgHandle":"inmem_6f9634bb,persist_f3035858",
                "ImgName":"vid-fr-inmem",
                "Sample_num":0,
                "Width":1920.0,
                "user_data":1
            }
         }
       ]  

   cam2 = [
           {
            "measurement": "camera",
            "fields": {
                "ImageStore": "1",
                "Cam_Sn":"cam2",
                "Channels":3.0,
                "Height":1200.0,
                "ImgHandle":"inmem_6f9634bb,persist_f3035858",
                "ImgName":"vid-fr-inmem",
                "Sample_num":0,
                "Width":1920.0,
                "user_data":-1
            }
         }
       ]    

   cam3 = [
           {
            "measurement": "camera",
            "fields": {
                "ImageStore": "1",
                "Cam_Sn":"cam3",
                "Channels":3.0,
                "Height":1300.0,
                "ImgHandle":"inmem_6f9634bb,persist_f3035858",
                "ImgName":"vid-fr-inmem",
                "Sample_num":0,
                "Width":1940.0,
                "user_data":1
            }
         }
       ]

   cam4 = [
           {
            "measurement": "camera",  # will add automatic 'time': '2019-03-28T16:42:18.262946335Z'
            #"timestamp": time.time(),
            #"time": str(datetime.datetime.now()),  # will save as '2019-03-28T22:02:03.788146944Z'
            "fields": {
                "ImageStore": "1",
                "Cam_Sn":"cam4",
                "Channels":3.0,
                "Height":1300.0,
                "ImgHandle":"inmem_6f9634bb,persist_f3035858",
                "ImgName":"vid-fr-inmem",
                "Sample_num":0,
                "Width":1940.0,
                "user_data":-1
            }
         }
       ]      
   """
   while True:
     write_points(client, cam1)
     write_points(client, cam2)
     write_points(client, cam3)
     write_points(client, cam4)
     time.sleep(5)
     read_data_points(client, {}, "camera")

esult: ResultSet({'('measurements', None)': [{'name': 'cam_serial1'}, {'name': 'cam_serial2'}, {'name': 'cam_serial3'}, {'name': 'cam_serial4'}, {'name': 'cam_serial5'}, {'name': 'cam_serial6'}]})
aafak2@aafak-ubuntu:~/Documents/python-exp$ 

  """


def main(host='localhost', port=8086):
    """Instantiate a connection to the InfluxDB."""
    user = 'admin'
    password = 'root'
    dbname = 'example'
    dbuser = 'smly'
    dbuser_password = 'my_secret_password'
    query = 'select value from cpu_load_short;'
    json_body = [
        {
            "measurement": "cpu_load_short",
            "tags": {
                "host": "server01",
                "region": "us-west"
            },
            "time": "2009-11-10T23:00:00Z",
            "fields": {
                "Float_value": 0.64,
                "Int_value": 3,
                "String_value": "Text",
                "Bool_value": True
            }
        }
    ]

    client = InfluxDBClient(host, port, user, password, dbname)

    print("Create database: " + dbname)
    client.create_database(dbname)

    print("Create a retention policy")
    client.create_retention_policy('awesome_policy', '3d', 3, default=True)

    print("Switch user: " + dbuser)
    client.switch_user(dbuser, dbuser_password)

    print("Write points: {0}".format(json_body))
    client.write_points(json_body)

    print("Querying data: " + query)
    result = client.query(query)

    print("Result: {0}".format(result))

    print("Switch user: " + user)
    client.switch_user(user, password)

    print("Drop database: " + dbname)
    client.drop_database(dbname)




"""
Refrences:
https://docs.influxdata.com/influxdb/v1.7/write_protocols/line_protocol_reference/#data-types

Queries:
https://docs.influxdata.com/influxdb/v1.7/write_protocols/line_protocol_reference/
https://github.com/intelsdi-x/snap-plugin-publisher-influxdb/issues/136

Database:
https://docs.influxdata.com/influxdb/v1.7/query_language/database_management/


Python example:
https://influxdb-python.readthedocs.io/en/latest/examples.html#tutorials-basic

"""

