download the dockerfile

```
mkdir jessica_dockder
cd jessica_dockder
wget https://raw.githubusercontent.com/gaoyuanliang/depression_patient_activity_dashboard/master/Dockerfile
```

download https://artifacts.elastic.co/downloads/kibana/kibana-6.7.1-linux-x86_64.tar.gz and unzip it to /Users/liangyu/Downloads/

download https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.7.1.tar.gz and unzip it to /Users/liangyu/Downloads/

build docker and rund the docker image
```bash
docker build -t jessica_kibana:1.0.1 .
docker run -it -v /Users/liangyu/Downloads/:/jessica/ -p 127.0.0.1:5601:5601 -p 127.0.0.1:9200:9200 --memory="256g" jessica_kibana:1.0.1
```

in docker run:

```bash
elasticsearch-6.7.1/bin/elasticsearch &
kibana-6.7.1-linux-x86_64/bin/kibana &
```

in docker try the service 

```bash
curl http://127.0.0.1:9200

{
  "name" : "lKx84gH",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "qxpQNOl4QQG7AdcodsgQTA",
  "version" : {
    "number" : "6.7.1",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "2f32220",
    "build_date" : "2019-04-02T15:59:27.961366Z",
    "build_snapshot" : false,
    "lucene_version" : "7.7.0",
    "minimum_wire_compatibility_version" : "5.6.0",
    "minimum_index_compatibility_version" : "5.0.0"
  },
  "tagline" : "You Know, for Search"
}

curl http://127.0.0.1:5601
```
