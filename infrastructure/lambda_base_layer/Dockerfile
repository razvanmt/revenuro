FROM --platform=linux/arm64 public.ecr.aws/lambda/python:3.10-arm64

# INSTALL PYTHON
RUN yum install -y python3 && \
    yum install -y python3-pip && \
    yum install -y zip && \
    yum clean all

# SET UP PIP AND VENV
RUN python3.10 -m pip install virtualenv
RUN python3.10 -m venv base
RUN source base/bin/activate

# INSTALL DEPENDENCIES
COPY ./requirements.txt .
RUN pip install -r requirements.txt -t ./python 

# ZIP IT UP FOR DEPLOYMENT
RUN zip -r layer.zip ./python/
ENTRYPOINT ["/bin/bash", "-1"]