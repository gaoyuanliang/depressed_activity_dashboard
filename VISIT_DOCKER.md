download https://artifacts.elastic.co/downloads/kibana/kibana-6.7.1-linux-x86_64.tar.gz and unzip it to /Users/liangyu/Downloads/

download https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.7.1.tar.gz and unzip it to /Users/liangyu/Downloads/

```bash
docker build -t jessica_kibana:1.0.1 .

docker run -it -v /Users/liangyu/Downloads/:/jessica/ -p 127.0.0.1:5601:5601 -p 127.0.0.1:9200:9200 --memory="256g" jessica_kibana:1.0.1
```

in docker run:

```bash
elasticsearch-6.7.1/bin/elasticsearch &
kibana-6.7.1-linux-x86_64/bin/kibana &
```
