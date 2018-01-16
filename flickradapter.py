# -*- coding: utf-8 -*-

import logging
import pickle


logger = logging.getLogger(__name__)

__FORMAT_VERSION__ = 1


def get_custom_size(sizes, size_requested, default='Large'):
    if size_requested in sizes:
        r = sizes[size_requested]
    elif default in sizes:
        logger.warning('size not found: %s, using default: %s',
                       size_requested, default)
        logger.warning('available sizes: %s', ', '.join(sizes.keys()))
        r = sizes[default]
    else:
        logger.warning('size not found: %s', size_requested)
        logger.warning('available sizes: %s', ', '.join(sizes.keys()))
        r = {'source': '', 'height': 0, 'width': 0, 'label': None}
    return r


def get_photo(photo_id, settings):
    api = settings['api_client']
    photo_id = int(photo_id)

    if api is None:
        logger.error('[flickreST]: Unable to get the Flickr API object')
        return None

    tmp_file = settings['FLICKR_REST_CACHE_LOCATION']
    size_alias = settings['FLICKR_REST_IMAGE_SIZE']

    try:
        with open(tmp_file, 'rb') as f:
            photo_mapping = pickle.load(f)
    except (IOError, EOFError, ValueError):
        photo_mapping = {}

    # Photo not in cache? Retrieve it and store it in cache.
    if photo_id not in photo_mapping:
        logger.info('[flickreST]: Fetching photo information for %s', photo_id)

        photo = api.Photo(id=photo_id)

        try:
            sizes = {x['label']: x for x in photo.getSizes()}
        except api.FlickrError as err:
            logger.error('[flickreST]: %s', err)
            return None

        photo_mapping[photo_id] = {
            'version': __FORMAT_VERSION__,
            'title': photo.title,
            'description': photo.description,
            'url': photo.url,
            'sizes': sizes,
        }

        with open(tmp_file, 'wb') as f:
            pickle.dump(photo_mapping, f)
    else:
        logger.info('[flickreST]: Using cached information')
        sizes = photo_mapping[photo_id]['sizes']

    # Data retrieved and cache. We are ready to send it back.
    size_detail = get_custom_size(sizes, size_alias)

    mphoto = photo_mapping[photo_id]
    r = {'title': mphoto['title'],
         'description': mphoto['description'],
         'url': mphoto['url'],
         'source_url': size_detail['source'],
         'width': size_detail['width'],
         'height': size_detail['height'],
         'size': size_detail['label']
         }

    return r
