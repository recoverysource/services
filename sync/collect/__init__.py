'''
Collect meeting data from remote sources
'''
import importlib
import logging
import re


class CollectionException(Exception):
    '''
    Fatal (semi-recoverable) feed import error
    '''
    pass


def fetch_all(source_data):
    '''
    Attempt to refresh all feeds found in source_data
    '''
    # Assemble list of remote sources
    sources = []
    for subdomain, data in source_data.items():
        if 'feed' not in data:
            continue
        if isinstance(data['feed'], list):
            for feed in data['feed']:
                sources.append(feed)
        else:
            sources.append(data['feed'])

    # Process feeds
    for source in sources:
        src_type, src_url = source.split('^')
        try:
            refresh(subdomain, src_url, src_type)
        except CollectionException as e:
            logging.warning(f'Feed import failed [{src_url}]: {e}')


def refresh(subdomain, source_url, source_type):
    '''
    Refresh meeting information from a source_url
    '''
    collector = importlib.import_module('.' + source_type, __name__)
    if not collector:
        raise Exception(f'Unable to load "{source_type}" collector.')
    return collector.grab(subdomain, source_url)


def validate(
        shortname: str,
        name: str,
        time: dict,
        tz: str,
        longitude: float,
        latitude: float,
        place: str = None,
        address: str = None,
        note: str = None,
        types: list = None,
        keywords: str = None,
        ) -> dict:
    '''
    Returns a dictionary that conforms to [aamod] spec
    aamod: https://handbook.recoverysource.net/template/meeting.html
    NOTE:  https://github.com/recoverysource/aamod/issues/15
    '''
    # Required fields:
    nf = {
            'shortname': shortname,
            'name': name,
            'longitude': longitude,
            'latitude': latitude,
            'timezone': tz,
            'time': time,
            }

    # Short alias for heavily used exception
    Invalid = CollectionException

    # Validate shortname
    if not re.match(r'^[a-z0-9\-\_]+$', shortname):
        raise Invalid(f'{shortname} must match [a-z0-9\\-_]+')

    # Validate name
    if not isinstance(name, str):
        raise Invalid(f'Invalid: {shortname}[name] must be a string')

    # Validate longitude
    if not isinstance(longitude, float):
        raise Invalid(f'Invalid: {shortname}[longitude] must be a float')

    # Validate latitude
    if not isinstance(latitude, float):
        raise Invalid(f'Invalid: {shortname}[latitude] must be a float')

    # Validate timezone
    if not isinstance(tz, str):
        raise Invalid(f'Invalid: {shortname}[timezone] must be a string')

    # Validate time
    for day, hours in time.items():
        if day not in ['Monday', 'Tuesday', 'Wednesday',
                       'Thursday', 'Friday', 'Saturday', 'Sunday']:
            raise Invalid(f'Invalid day in {shortname}[time]')
        if not isinstance(hours, list):
            raise Invalid(f'Invalid: {shortname}[time] must be dict/lists')

    # Validate place
    if place:
        if not isinstance(place, str):
            raise Invalid(f'Invalid: {shortname}[place] must be a string')
        nf['place'] = place

    # Validate address
    if address:
        if not isinstance(address, str):
            raise Invalid(f'Invalid: {shortname}[address] must be a string')
        nf['address'] = address

    # Validate note
    if note:
        if not isinstance(note, str):
            raise Invalid(f'Invalid: {shortname}[note] must be a string')
        nf['note'] = note

    # Validate types
    if types:
        if not isinstance(types, list):
            raise Invalid(f'Invalid: {shortname}[types] must be a list')
        nf['types'] = types

    # Validate keywords
    if keywords:
        if not isinstance(keywords, str):
            raise Invalid(f'Invalid: {shortname}[keywords] must be a string')
        nf['keywords'] = keywords

    # Return normalized and validated data
    return nf
