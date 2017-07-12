#!/usr/bin/env python
'''
################################################################################
# Copyright (c) 2013, 2016, 2017 Genome Research Ltd.
#
# Author: Peter Clapham <pc7@sanger.ac.uk>, John Constable <jc18@sanger.ac.uk>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
################################################################################


This script is documented within the associated README.md.
It is are provided as a skeleton starting point for other
projects.

an example AMQP reader to collect successful
job data from a Rabbit AMQP LSF job queue
'''

import pika
import json
from os.path import expanduser


COUNT = 0


def callback(ch, method, properties, body):
    if "job" in body:
    #if "Success" in body:
        global COUNT
        COUNT += 1
        print " [x] Received %r %d" % (body, COUNT)

if __name__ == '__main__':

    home = expanduser("~")
    with open(home + "/.config/lsf_log_watch/config.json") as config_file:
        config = json.load(config_file)

    credentials = pika.credentials.PlainCredentials(config['amqp_user'], config['amqp_password'])
    parameters = pika.ConnectionParameters(
        config['amqp_server'],
        5672,
        '/',
        credentials)

    connection = pika.adapters.blocking_connection.BlockingConnection(parameters=parameters)
    channel = connection.channel()
    channel.queue_declare(queue='Finish')

    channel.basic_consume(callback,
                          queue='Finish',
                          no_ack=True)
    channel.start_consuming()
