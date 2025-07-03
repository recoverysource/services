'''
Collect meeting data from TSML
'''
import hashlib
import json
import logging
import re
import requests
import urllib.parse

import sync.collect
import sync.db


# Pattern(s) to identify TSML-UI source data
TSML_JSON = (
        r'<div id="tsml-ui"\s+'
        r'data-src="([^"]+\.json)[0-9?]*"\s+'
        r'data-timezone="([^"]+)"')
TSML_FEED = (
        r'<link\s+rel="alternate"\s+'
        r'type="application/json"\s+'
        r'title="Meetings Feed"\s+href="([^"]+)"')

# Map numbers to days of week
DAYS_OF_WEEK = {
        0: 'Sunday',
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday',
        7: 'Sunday'}


def grab(subdomain, source_url):
    '''
    Refresh collected data from a remote Twelve-Step-Meeting-List (TSML) source
    '''
    # Fetch current meeting (tsml-ui) page
    response = get(source_url)
    if response.status_code != 200:
        raise sync.collect.CollectionException(
                f'Unexpected response [{response.status_code}]')

    # Identify url for source data from feed and fetch json
    source = urllib.parse.urlparse(source_url)
    if match := re.search(TSML_JSON, response.text):
        source_data = fetch_json(
                f'{source.scheme}://{source.netloc}{match.group(1)}')
        data_timezone = match.group(2)
    elif match := re.search(TSML_FEED, response.text):
        source_data = fetch_json(match.group(1))
        # TODO
        data_timezone = 'TODO'
    else:
        raise sync.collect.CollectionException('No TSML source data found')

    # Normalize TSML source data
    collected = normalize(source_data, data_timezone)

    # Store collected data
    for slug, meeting in collected.items():
        # Create string from validated (merged) meeting data
        geostore = json.dumps(sync.collect.validate(shortname=slug, **meeting))
        # Save data into database
        sync.db.geo_set(
                key=f'{subdomain}_{slug}',
                lon=meeting['longitude'],
                lat=meeting['latitude'],
                value=geostore)


def get(url):
    '''
    Add options to ensure get requests succeed
    '''
    return requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',  # noqa: E501
        })


def fetch_json(source_url):
    '''
    Return TSML data from a plain json url
    '''
    # Cache ID based on checksum of URL
    url_checksum = hashlib.sha256(source_url.encode('utf-8')).hexdigest()

    # Check if this json file has already been cached
    if sync.db.exists(url_checksum):
        logging.debug(f'{source_url} exists in cache; using local copy')
        return json.loads(sync.db.get(url_checksum))

    # Download TSML data
    response = get(source_url)
    if response.status_code != 200:
        raise sync.collect.CollectionException(
                f'Unexpected response for json [{response.status_code}]')
    sync.db.set(url_checksum, response.content)
    logging.debug(f'Collected meeting data from {source_url}')
    return response.json()


def normalize(source_data, default_tz):
    '''
    Returns a dictionary of data normalized according to AAMod [spec]
    [spec]: https://handbook.recoverysource.net/module/format.html
    '''
    normalized = {}
    for meeting in source_data:
        # Check for required fields
        missed_fields = []
        for required in ['name', 'day', 'types']:
            if meeting.get(required) is None:
                missed_fields.append(required)
        if missed_fields:
            logging.info(f'Skip {meeting["name"]}; missing {missed_fields}')
            logging.debug(f'Skipped Meeting: {meeting}')
            continue

        if meeting['slug'] not in normalized:
            # Populate with initial data
            # TODO: slug is bad; must be customized
            normalized[meeting['slug']] = {
                    'name': meeting['name'],
                    'time': {},
                    # 'place': meeting[''],
                    'tz': meeting.get('timezone', default_tz),
                    'address': meeting['formatted_address'],
                    'longitude': meeting['longitude'],
                    'latitude': meeting['latitude'],
                    'types': meeting['types'],
                    }

            # Optional values
            if meeting.get('notes'):
                normalized[meeting['slug']]['note'] = meeting['notes']
            if meeting.get('location') or meeting.get('region'):
                normalized[meeting['slug']]['keywords'] = '{} {}'.format(
                        meeting.get('location', ''),
                        meeting.get('region', ''))

        # Add meeting time to existing entry
        cm = normalized[meeting['slug']]
        day = DAYS_OF_WEEK[meeting['day']]
        if day not in cm['time']:
            cm['time'][day] = [meeting['time']]
        else:
            cm['time'][day].append(meeting['time'])

    return normalized
