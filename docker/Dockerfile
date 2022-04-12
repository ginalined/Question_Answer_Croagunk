# Ubuntu Linux as the base image
FROM ubuntu:22.04

# Set UTF-8 encoding
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Install Python
RUN apt-get -y update && \
    apt-get -y upgrade

# The following line ensures that subsequent install doesn't expect user input
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y install python3-pip python3-dev

# Install nlp libraries
RUN pip3 install --upgrade pip
RUN pip3 install stanza
RUN pip3 install nltk
RUN pip3 install pandas

# Add the files into QA
RUN mkdir /QA/
# COPY . /QA
RUN mkdir -p /QA/question
RUN mkdir -p /QA/processor
# RUN mkdir -p /QA/data
# ADD test_questions.txt /QA
ADD ask /QA
ADD answer /QA
ADD ans/how_what_why_answer.py /QA/ans
ADD ans/who_when_where_answer.py /QA/ans
ADD ans/yes_no_answer.py /QA/ans
ADD question/yes_no_question.py /QA/question
ADD question/wh_question.py /QA/question
ADD processor/stanza_process.py /QA/processor
# ADD data /QA/data
ADD setup.py /QA
# ADD test.sh /QA
RUN python3 /QA/setup.py

# Change the permissions of programs
CMD ["chmod 777 /QA/*"]

# Set working dir
WORKDIR /QA
ENTRYPOINT ["/bin/bash", "-c"]