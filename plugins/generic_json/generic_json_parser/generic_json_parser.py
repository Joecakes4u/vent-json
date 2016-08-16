
#!/usr/bin/env python
#
#   Copyright (c) 2016 In-Q-Tel, Inc, All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


"""
Generic JSON parser plugin

Created on  4 August 2016
@author: Joe Wonohadidjojo
"""

import json
import pika
import subprocess
import sys

def get_path():
    path = None
    try:
        path = sys.argv[1]
    except:
        print "no path provided, quitting."
    return path

def connections():
    """Handle connection setup to rabbitmq service"""
    channel = None
    connection = None
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='rabbitmq'))
        channel = connection.channel()

        channel.exchange_declare(exchange='topic_recs',
                                 type='topic')
    except:
        print "unable to connect to rabbitmq, quitting."
    return channel, connection


def run_tool(path):
    """Tool entry point"""
    routing_key = "generic_json_parser"+path.replace("/",".")
    channel, connection = connections()
    print "sending JSON..."
    try:
        with open(path, 'r') as f:
            recs = []
            try:
                recs = json.load(f)
            except:
                for line in f:
                    recs.append(json.loads(line))
            try:
                for rec in recs:
                    message = str(rec)
                    if channel:
                        channel.basic_publish(exchange='topic_recs', routing_key=routing_key,body=message)
                        print " [x] Sent %r:%r" % (routing_key, message)
            except Exception as e:
                pass
    except Exception as e:
        pass

    try:
        connection.close()
    except:
        pass

if __name__ == '__main__':
    path = get_path()
    if path:
        run_tool(path)
