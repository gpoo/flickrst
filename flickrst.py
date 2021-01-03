# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from docutils import nodes
from docutils.parsers.rst import directives, Directive

from pelican import signals
from flickrst import flickradapter, flickr


default_template = """
    <div class="{{class}}">
      <figure class="{{figclass}}">
        <a href="{{url}}">
        <img alt="{{alt}}"
             src="{{raw_url}}"
             {% if FLICKR_REST_INCLUDE_DIMENSIONS %}width="{{width}}"
             height="{{height}}"
             {% endif %}/></a>
        <figcaption>{{caption}}</figcaption>
      </figure>
    </div>"""

logger = logging.getLogger(__name__)


def setup_settings(pelican):
    """Add Flickr api object to Pelican settings."""

    Flickr.SETTINGS = {}

    for key in ('TOKEN', 'KEY', 'SECRET'):
        try:
            value = pelican.settings['FLICKR_API_' + key]
            setattr(flickr, 'API_' + key, value)
        except KeyError:
            logger.warning('[flickrst]: FLICKR_API_%s is not defined ' +
                           'in the configuration', key)

    Flickr.SETTINGS['api_client'] = flickr

    pelican.settings.setdefault(
        'FLICKR_REST_CACHE_LOCATION',
        '/tmp/org.calcifer.flickrest-images.cache')
    pelican.settings.setdefault('FLICKR_REST_IMAGE_SIZE', 'Medium 640')
    pelican.settings.setdefault('FLICKR_REST_INCLUDE_DIMENSIONS', True)

    for suffix in 'CACHE_LOCATION', 'IMAGE_SIZE', 'INCLUDE_DIMENSIONS':
        key = 'FLICKR_REST_%s' % suffix
        Flickr.SETTINGS[key] = pelican.settings[key]


class Flickr(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
                   'alt': directives.unchanged,
                   'class': directives.unchanged,
                   'figclass': directives.unchanged,
                   'size': directives.unchanged,
                   }
    has_content = True
    generator = None

    def run(self):
        """Include a file as part of the content of this reST file."""

        from jinja2 import Template

        flickr_id = self.arguments[0]
        template = Template(default_template)
        options = {
           'class': 'div-container',
           'figclass': 'figure-container',
           'url': 'https://flickr.com/',
           'raw_url': None,
           'alt': None,
           'width': None,
           'height': None,
           'caption': 'caption',
        }

        options.update(self.options)

        if self.content:
            node = nodes.Element()          # anonymous container for parsing
            self.state.nested_parse(self.content, self.content_offset, node)
            first_node = node[0]

            if isinstance(first_node, nodes.paragraph):
                options['caption'] = first_node.astext()
            elif not (isinstance(first_node, nodes.comment)
                      and len(first_node) == 0):
                error = self.state_machine.reporter.error(
                      'Figure caption must be a paragraph or empty comment.',
                      nodes.literal_block(self.block_text, self.block_text),
                      line=self.lineno)
                return [nodes.raw('', '', format='html'), error]

            if len(node) > 1:
                text = [n.astext() for n in node[1:] if isinstance(n, nodes.paragraph)]
                options['caption'] = ' '.join([options['caption']] + text)
                logger.warning('[flickrst]: Text after the first ' +
                             'paragraph is merged with the caption ' +
                             'as one single paragraph.')

        if self.SETTINGS['api_client'] is None:
            logger.error('[flickrst]: Unable to get the Flickr API object.')
            replacement = template.render(options)
            return [nodes.raw('', replacement, format='html')]

        if 'size' in options:
            self.SETTINGS['FLICKR_REST_IMAGE_SIZE'] = options['size']

        info = flickradapter.get_photo(flickr_id, self.SETTINGS)

        if info:
            options['raw_url'] = info['source_url']
            options['url'] = info['url']
            options['width'] = info['width']
            options['height'] = info['height']
            options['FLICKR_REST_INCLUDE_DIMENSIONS'] = self.SETTINGS['FLICKR_REST_INCLUDE_DIMENSIONS']

        replacement = template.render(options)
        result = nodes.raw('', replacement, format='html') 
        # logger.debug('[flickrst]: ' + result.astext())

        return [result]


def register():
    signals.initialized.connect(setup_settings)
    directives.register_directive('flickr', Flickr)
