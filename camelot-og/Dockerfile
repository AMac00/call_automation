#####################################################################################################################
# This is the Docker file needed for Docker build of camelot-og untested/tested setup.
# Author: shivvat <shihashi@cisco.com>
#####################################################################################################################

FROM rcdn6-vm67-9.cisco.com/cbase:latest
MAINTAINER Camelot Dev <camelot-dev@cisco.com>


#RUN wget http://wwwin-vts.cisco.com/camelot/installers/CoC-11.5.0.0.3.0L-1.x86_64.rpm
ADD CAMELOT_RPM_FILE /tmp/
WORKDIR /tmp/
RUN yum -y install CAMELOT_RPM_FILE

ENV CAMELOT_LOGS /var/camelot/logs
ENV CAMELOT_LIB /usr/local/camelot/lib

EXPOSE 5000
# note: using an entry point instead of CMD allows us to start Camelelot with different command line parameters.
ENTRYPOINT ["camserv","-vp","5000"]

# Create Camelot coredump dir
RUN mkdir -p /var/crash
