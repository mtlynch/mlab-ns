#! /usr/bin/env python

import ConfigParser
import logging
import urllib
import urllib2
from optparse import OptionParser
from os import path
from os import access
from os import R_OK

from mlabns.util import request_validation

class RegistrationClient:
    """Sends HTTP POST requests."""

    def __init__(self):
        self.key = None
        self.server_url = None
        self.requests = []
        logging.basicConfig(
            format='[%(asctime)s] %(levelname)s: %(message)s',
            level=logging.DEBUG)

    def read_configuration(self, config_file):
        """Reads configuration file.
         
        [server_url]
        server_url: http://localhost:8080/register

        [key]
        key: mlab-ns@admin

        [npad.iupui.mlab1.ath01.measurement-lab.org]
        entity: sliver_tool
        tool_id:	npad
        node_id: mlab1.ath01.measurement-lab.org
        sliver_tool_id:	npad.iupui.mlab1.ath01.measurement-lab.org
        sliver_tool_key: npad.iupui.key
        sliver_ipv4: 83.212.4.12
        sliver_ipv6: off 
        url: http://npad.iupui.mlab1.ath01.measurement-lab.org:8000
        status: init
        
        ...
    
        [npad.iupui.mlab1.atl01.measurement-lab.org]
        entity: sliver_tool
        tool_id:	npad
        node_id: mlab1.atl01.measurement-lab.org
        sliver_tool_id:	npad.iupui.mlab1.atl01.measurement-lab.org
        sliver_tool_key: npad.iupui.key
        sliver_ipv4: 4.71.254.138
        sliver_ipv6: off 
        url: http://npad.iupui.mlab1.atl01.measurement-lab.org:800
        status: init
    
        Args:
          config_file: A file containing the data configuration.
        """
        config = ConfigParser.ConfigParser()
        try:
            config.read(config_file)
            # TODO(claudiu): If the configuration file is not passed 
            # as an argument use a default location e.g.'/etc/mlab-ns.conf'.
        except ConfigParser.Error, e:
            # TODO(claudiu) Trigger an event/notification.
            logging.error('Cannot read the configuration file: %s.', e)
            exit(-1)
        
        for section in config.sections():
            if section == 'key':
                self.key = config.get(section, 'key')
            elif section == 'server_url':
                self.server_url = config.get(section, 'server_url')
            else:
                logging.info('BEGIN %s', section)
                request = {}
                for option in config.options(section):
                    request[option] = config.get(section, option)
                    logging.info(
                        '%s = "%s"',
                        option,
                        config.get(section, option))    
                logging.info('END %s\n.', section)
                request['timestamp'] = request_validation.generate_timestamp()
                signature = request_validation.sign(request, self.key)
                request['sign'] = signature
                self.requests.append(request)

        if self.key is None or self.server_url is None:
            logging.error('Missing key or server_url.')
            exit(-1)

    def send_requests(self):
        """Sends the requests to the server."""

        url = self.server_url
        for request in self.requests:
            data = urllib.urlencode(request)
            req = urllib2.Request(url, data)
            logging.info('Request:')
            for key in request.keys():
                logging.info('data[%s] = "%s"', key, request[key])
            
            logging.info('Sending...\n')
            try:
                response = urllib2.urlopen(req)
                logging.info('Response: %s\n', response.read())
            except urllib2.URLError, e:
                # TODO(claudiu) Trigger an event/notification.
                logging.error('Cannot send request: %s.\n', e)

def main():
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s: %(message)s',
        level=logging.DEBUG)

    parser = OptionParser()
    parser.add_option(
    '-f',
    '--file',
    dest='filename',
    help='configuration file')

    (options, args) = parser.parse_args()
    if options.filename is None:
        # TODO(claudiu) Trigger an event/notification.
        logging.error('Missing configuration file.')
        parser.print_help()
        exit(-1)

    config_file = options.filename  
    if  not path.exists(config_file):
        # TODO(claudiu) Trigger an event/notification.
        logging.error('%s does not exist.', config_file)
        exit(-1)

    if not path.isfile(config_file):
        # TODO(claudiu) Trigger an event/notification.
        logging.error('%s is not a file.', config_file)
        exit(-1)
 
    if not access(config_file, R_OK):
        # TODO(claudiu) Trigger an event/notification.
        logging.error('Cannot read %s.', config_file)
        exit(-1)

    client = RegistrationClient()
    client.read_configuration(config_file)
    client.send_requests()

if __name__ == '__main__':
    main()
