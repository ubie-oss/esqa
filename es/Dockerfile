FROM docker.elastic.co/elasticsearch/elasticsearch-oss:7.10.2
ENV discovery.type single-node

# kuromojiをインストール
RUN elasticsearch-plugin  install analysis-kuromoji

# icuをインストール
RUN elasticsearch-plugin  install analysis-icu

ADD ./config/elasticsearch.yml /usr/share/elasticsearch/config/
ADD ./config/log4j2.properties /usr/share/elasticsearch/config/

USER root
RUN chown elasticsearch:elasticsearch config/log4j2.properties config/elasticsearch.yml 

USER elasticsearch
