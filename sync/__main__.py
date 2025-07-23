#!/usr/bin/env python3
'''
Utility script to perform synchronization operations for sober.page URLs.

See "options.py" or "python3 -m sync --help" for usage.
'''
import logging

# Local imports
import sync.db
import sync.collect
import sync.hugo
import sync.nginx
import sync.named
import sync.options


def main():
    '''
    Primary script logic
    '''
    # Read command line arguments
    options = sync.options.parser().parse_args()

    # Set log level (from options)
    logging.getLogger().setLevel(options.loglevel.upper())

    # Load source data from hugo
    logging.debug(f'Reading input data from {options.hugo_data}')
    hugo_data = sync.hugo.load_yaml(options.hugo_data)
    source_data = sync.hugo.normalize(hugo_data)

    # Connect to database if needed by action(s) [-c,]
    # if (options.collect):
    #     sync.db.open(f'{options.local_data}/cache.db')

    # [-c] Collect meeting data from remote feeds
    # if options.collect:
    #     logging.info('Collecting meeting data')
    #     sync.collect.fetch_all(source_data)

    # [-n] Generate an nginx map file
    if options.mapfile:
        logging.info(f'Generating nginx map file at {options.mapfile}')
        sync.nginx.make_map(source_data, options.mapfile)

    # [-z] Generate a bind9 zone file
    if options.zonefile:
        logging.info(f'Generating zone file at {options.zonefile}')
        sync.named.make_zone(source_data, options.zonefile)


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s: %(message)s')
    main()
