*THIS IS A WORK IN PROGESS*
===========================

```
IBM Platform LSF is a powerful workload management platform for demanding, 
distributed HPC environments. It provides a comprehensive set of intelligent,
policy-driven scheduling features that enable you to utilise all of your 
compute infrastructure resources and ensure optimal application performance.

Obtaining job status is usually via poll based bjobs requests. As clusters and
user numbers continue to grow, this process becomes limiting and not a 
practical programmtic interface for workload management, pipeline development
or cluster monitoring.

This script should provide job data directly from the lsb.acct file. All 
LSF status data is captured, along with job resource usage and requirements, 
which are sent to an AMQP queue.
```

Setup
=====

A functioning Rabbit AMQP server with configured accounts and basic queue 
in place. The AMQP setup is outside the scope here.  
Please refer to www.rabbitmq.com for AMQP consumer example code.

The platform python LSF api is available from here:
https://github.com/PlatformLSF/platform-python-lsf-api


Recommended run methodology
==========================

Configure virtualenv
--------------------


Install virtualenv within your local environment and add the required python
lsf api, pika, etc modules to your virtualenv (the included requirements.txt file does this for you. 

NB pythonlsf requires lsf headers and libraries to be available on the host for installation to succeed.

python lsf documentation can be found here:
https://github.com/PlatformLSF/platform-python-lsf-api

source and confirm that these work as expected with:

```
#ensure you are doing this with the LSF environment variables already defined
virtualenv <virtualenv_dir>
source <virtualenv_dir>/bin/activate
pip install -r requirements.txt
```

Create an ~/.config/lsf_log_watch/config.json to reflect local lsb.acct location and AMQP server 
connection details and credentials, e.g.

```
{

    "lsb_acct_path": "/usr/local/lsf/work/farm3/logdir/lsb.acct",
    "amqp_server": "amqp-srv1",
    "amqp_user": "john",
    "amqp_password": "itsasecretinit"
    
}
```


Server to push logs to RabbitMQ/AMQP server
-------------------------------------------

The lsf_log_watch.py script requires a host running LSF 9.x with read access 
to lsb.streams and the IBM platform python api installed. 

`<virtualenv_dir>/bin/python ./lsf_log_watch.py &`


Example Reader
--------------

```
<virtualenv_dir>/bin/python ./reader_example.py
 [x] Received '{"jobId": 2909824, "numProcessors": 1, "resReq": "select[mem>8000] rusage[mem=8000]", "avgMem": 1795341504, "GMendTime": "2017-07-11 08:36:49", "maxRMem": 31744, "job": "Success", "startTime": 1499762207, "jStatus": 64, "termTime": 0, "runTime": 2, "userName": "bob", "runLimit": -1, "idx": 34, "exitInfo": 0, "cpuTime": 0.9840610027313232, "jobName": "contam_screen_TMU[1-78]", "queue": "long", "endTime": 1499762209, "exitStatus": 0, "options": 33817107, "exceptMask": 4}' 1
 ...
```
