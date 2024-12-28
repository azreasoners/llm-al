# Use Ubuntu 18.04 as the base image
FROM ubuntu:18.04

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    git \
    gcc \
    g++ \
    autoconf \
    automake \
    libtool \
    make \
    zlib1g-dev \
    libffi-dev \
    libssl-dev \
    libsqlite3-dev \
    flex \
    bison \
    re2c \
    libboost-dev=1.65.1.0ubuntu1 \
    libboost-system-dev \
    libboost-filesystem-dev \
    libboost-iostreams-dev \
    libboost-thread-dev \
    libboost-program-options-dev \
    libboost-timer-dev \
    && wget https://www.python.org/ftp/python/3.11.4/Python-3.11.4.tgz \
    && tar xzf Python-3.11.4.tgz \
    && cd Python-3.11.4 \
    && ./configure \
    && make \
    && make install \
    && cd .. \
    && rm -rf Python-3.11.4*

# Install clingo using conda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /miniconda.sh \
    && bash /miniconda.sh -b -p /opt/conda \
    && rm /miniconda.sh \
    && /opt/conda/bin/conda config --add channels potassco \
    && /opt/conda/bin/conda create -y --name llm-al python=3.11 \
    && /opt/conda/bin/conda run -n llm-al conda install -y -c potassco clingo \
    && /opt/conda/bin/conda run -n llm-al conda install -y numpy \
    && /opt/conda/bin/conda init bash

# Automatically activate llm-al environment on container start
RUN echo "source /opt/conda/etc/profile.d/conda.sh && conda activate llm-al" >> ~/.bashrc

# Set environment variable for Boost
ENV boost_cv_lib_version=1_65_1

# Clone and install Cplus2ASP
RUN git clone https://github.com/azreasoners/Cplus2ASP.git /Cplus2ASP \
    && cd /Cplus2ASP \
    && gcc externals/f2lp/f2lp.c -o f2lp \
    && cp f2lp /usr/local/bin/ \
    && ./bootstrap.sh \
    && make \
    && make install \
    && mv /usr/local/bin/cplus2asp4 /usr/local/bin/cplus2asp

# Install Python dependencies
#RUN python3.11 -m pip install --no-cache-dir openai==0.27
RUN /opt/conda/bin/conda run -n llm-al pip install openai==0.27


# Set working directory
WORKDIR /app

# Copy the Python code into the container
#COPY . /app
COPY ./app /app

# Default command to keep the container running interactively
CMD ["bash", "-l"]

