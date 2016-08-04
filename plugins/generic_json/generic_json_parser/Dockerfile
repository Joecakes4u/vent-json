FROM ubuntu:16.04
MAINTAINER Joe Wonohadidjojo <joecakes4u@gmail.com>

RUN apt-get update

ADD . /generic_json_parser
WORKDIR /generic_json_parser

ENTRYPOINT ["python", "generic_json_parser.py"]
CMD[""]
