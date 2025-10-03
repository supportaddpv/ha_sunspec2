ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Install requirements for add-on
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-setuptools \
    py3-wheel

# Copy data for add-on
COPY requirements.txt /tmp/
COPY sunspec2/ /opt/sunspec2/
COPY setup.py /opt/
COPY run.sh /
COPY app.py /

# Install Python dependencies
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt && \
    pip3 install --no-cache-dir paho-mqtt

# Make run script executable
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
