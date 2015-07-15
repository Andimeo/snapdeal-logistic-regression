FROM ubuntu

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 627220E7
RUN echo 'deb http://archive.scrapy.org/ubuntu scrapy main' | sudo tee /etc/apt/sources.list.d/scrapy.list
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y scrapy-0.24 python-pip python-dev libmysqlclient-dev
RUN mkdir /spider-run

COPY data_preprocess /spider-run/data_preprocess
COPY snapdeal_spider /spider-run/snapdeal_spider

WORKDIR /spider-run/snapdeal_spider

ENTRYPOINT ["scrapy"]
CMD ["crawl", "snapdeal_spider", "-a", "queries=/spider-run/data_preprocess/queries", "-o", "items.csv"]
