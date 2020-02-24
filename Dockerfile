FROM ubuntu:18.04

# Copy all files!
ENV HOME_PATH=/home/program/
RUN mkdir -p $HOME_PATH
COPY ./ $HOME_PATH


# Install needed programs
RUN apt-get update && \
	  apt-get install -y \
		curl \
    nano \
		libsm6 \
		libxext6 \
		libxrender-dev \
    python3-pip \
    python3-dev  && \
    apt-get -y autoremove && \
    rm -rf /var/lib/apt/lists/*

# Install python packages
RUN pip3 install -r /home/program/requirements.txt --no-cache-dir

CMD python3 /home/program/main.py
