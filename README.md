# Depression Patient Activity Dashboard

Building a Kibana dashboard to analyze the activity sensor data collected from patients suffering from depression. 

The data introduction is at https://datasets.simula.no/depresjon/

## Instillation 

### Instilling Elasticsearch and Kibana

```bash
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.7.1.tar.gz
tar -xf elasticsearch-6.7.1.tar.gz
cd elasticsearch-6.7.1
bin/elasticsearch
```

```bash
wget https://artifacts.elastic.co/downloads/kibana/kibana-6.7.1-darwin-x86_64.tar.gz
tar -xf kibana-6.7.1-darwin-x86_64.tar.gz
cd kibana-6.7.1-darwin-x86_64
bin/kibana
```

then you can view the kibana dashboard at http://localhost:5601

## Installing this package

```bash
git clone https://github.com/gaoyuanliang/depression_patient_activity_dashboard.git
cd depression_patient_activity_dashboard
pip3 install -r requirements.txt
```

## Downloading the data

```bash
wget https://datasets.simula.no/depresjon/data/depresjon-dataset.zip
unzip depresjon-dataset.zip
```

## Process, merge, enrich, and ingest the data to Elastic search 

```bash
python3 deep_depression_detector_data_visulize.py
```

## Building the dashboard

<img src="https://raw.githubusercontent.com/gaoyuanliang/deep_depression_detector/master/ezgif-2-9ca41a12826a.gif" width="1000">

<img src="https://raw.githubusercontent.com/gaoyuanliang/deep_depression_detector/master/screencapture-localhost-5601-app-kibana-2020-08-31-21_42_09.png" width="500"> <img src="https://raw.githubusercontent.com/gaoyuanliang/deep_depression_detector/master/screencapture-localhost-5601-app-kibana-2020-08-31-21_43_31.png" width="500">
