
FROM tiangolo/uwsgi-nginx-flask:python3.7

# Update to the latest PIP
RUN pip3 install --upgrade pip


# Set the current working directory
WORKDIR /app

# Copy files into the current working directory WORKDIR
COPY ./ ./

# install our dependencies
RUN  pip3 install -r requirements.txt