FROM debian:latest
MAINTAINER Fernando Costantini <fhcostantini@gmail.com>


RUN apt-get update && apt-get install git python2.7 curl vim wget --force-yes -y 


ENV CLOUDSDK_PYTHON python2.7
RUN curl https://sdk.cloud.google.com | bash


RUN echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" | tee /etc/apt/sources.list.d/webupd8team-java.list
RUN echo "deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" | tee -a /etc/apt/sources.list.d/webupd8team-java.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys EEA14886 
RUN apt-get update
RUN echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections
RUN echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections
RUN DEBIAN_FRONTEND=noninteractive  apt-get install -y --force-yes oracle-java8-installer oracle-java8-set-default 
RUN rm -rf /var/cache/oracle-jdk8-installer  && apt-get clean  && rm -rf /var/lib/apt/lists/*


RUN export DEBIAN_FRONTEND=noninteractive && \
	sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
	apt-get update && \
	apt-get -y upgrade && \
	apt-get install -y maven
