#!/usr/bin/env python2

import os
import sched
import time
import jinja2

from gandi_dyndns import update_ip

import logging as log
log.basicConfig(format='%(asctime)-15s [%(levelname)s] %(message)s', level=log.DEBUG)

CONFIG_PATH = './config.json'
SLEEP = 300  # In second

# If we cannot find a config file we generate it
if not os.path.isfile(CONFIG_PATH):
    log.info('Starting for the first time...')
    path, filename = os.path.split('config-template.j2')

    context = {
        "api_key": os.getenv('API_KEY', "yourtwentyfourcharapikey"),
        "domain":  os.getenv('DOMAIN', "example.com"),
        "subdomains": map(lambda s: "\"{}\"".format(s.strip()), os.getenv('SUBDOMAINS', "dynamic, @, mail, xmpp").split(","))
    }

    config_content = jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)

    with open(CONFIG_PATH, "w") as config_file:
        config_file.write(config_content)
        log.info('Configuration ready!')


# Run gandi_dyndns every once in a while
s = sched.scheduler(time.time, time.sleep)
def do_run(sc):
    update_ip()
    s.enter(SLEEP, 1, do_run, (sc,))

s.enter(SLEEP, 1, do_run, (s,))
s.run()
