FROM ubuntu:18.04 as build_stage

RUN apt-get update

ARG GDAL_VERSION=2.4.2
ARG PROJ_VERSION=6.0.0

RUN apt-get -y install build-essential libgeos-dev sqlite3 libsqlite3-dev \
    pkg-config python3 python3-dev libgdal-dev wget bzip2
ENV CXX="g++ -std=c++98"  

############################## Build Proj ##########################################
RUN cd /tmp/ && \
    wget http://download.osgeo.org/proj/proj-${PROJ_VERSION}.tar.gz && \
    tar xvf proj-${PROJ_VERSION}.tar.gz && \
    cd /tmp/proj-${PROJ_VERSION} && \
    ./configure
RUN cd /tmp/proj-${PROJ_VERSION} && \
    make -j$(nproc)
RUN mkdir /tmp/build_proj 
RUN cd /tmp/proj-${PROJ_VERSION} && \
    make install DESTDIR="/tmp/build_proj"
RUN cp /tmp/proj-${PROJ_VERSION}/src/.libs/libproj.so.15 /usr/lib/libproj.so.15
RUN cp /tmp/proj-${PROJ_VERSION}/src/.libs/libproj.so /usr/lib/libproj.so

############################## Build GDAL ##########################################
RUN cd /tmp/ && \
    wget http://download.osgeo.org/gdal/${GDAL_VERSION}/gdal-${GDAL_VERSION}.tar.gz && \
    tar xvfz gdal-${GDAL_VERSION}.tar.gz && \
	cd /tmp/gdal-${GDAL_VERSION} && \
	./configure --with-python --with-proj=yes --with-png=internal --with-geos=yes --with-threads=yes
RUN cd /tmp/gdal-${GDAL_VERSION} && \
    make -j2
RUN mkdir /tmp/build
RUN cd /tmp/gdal-${GDAL_VERSION} && \
    make install DESTDIR="/tmp/build" 
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
RUN cd /tmp/gdal-${GDAL_VERSION}/swig/python && python3 setup.py install


FROM ubuntu:18.04 as runner_stage

RUN apt-get update
RUN apt-get install -y python3 python3-pip libgdal-dev rar unrar

COPY --from=build_stage /tmp/build_proj/usr/local/share/proj/ /usr/local/share/proj/
COPY --from=build_stage /tmp/build_proj/usr/local/include/ /usr/local/include/
COPY --from=build_stage /tmp/build_proj/usr/local/bin/ /usr/local/bin/
COPY --from=build_stage /tmp/build_proj/usr/local/lib/ /usr/local/lib

COPY --from=build_stage /tmp/build/usr/local/share/gdal/ /usr/local/share/gdal/
COPY --from=build_stage /tmp/build/usr/local/include/ /usr/local/include/
COPY --from=build_stage /tmp/build/usr/local/bin/ /usr/local/bin/
COPY --from=build_stage /tmp/build/usr/local/lib/ /usr/local/lib/

RUN pip3 install gdal==2.4
RUN pip3 install vectorio
RUN ldconfig
CMD python3