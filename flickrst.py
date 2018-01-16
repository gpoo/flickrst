# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from docutils import nodes
from docutils.parsers.rst import directives, Directive

from pelican import signals
from flickrst import htmlnodes, flickradapter, flickr


logger = logging.getLogger(__name__)


def setup_settings(pelican):
    """Add Flickr api object to Pelican settings."""

    Flickr.SETTINGS = {}

    for key in ('TOKEN', 'KEY', 'SECRET'):
        try:
            value = pelican.settings['FLICKR_API_' + key]
            setattr(flickr, 'API_' + key, value)
        except KeyError:
            logger.warning('[flickreST]: FLICKR_API_%s is not defined ' +
                           'in the configuration', key)

    Flickr.SETTINGS['api_client'] = flickr

    pelican.settings.setdefault(
        'FLICKR_REST_CACHE_LOCATION',
        '/tmp/org.calcifer.flickrest-images.cache')
    pelican.settings.setdefault('FLICKR_REST_IMAGE_SIZE', 'Medium 640')

    for suffix in 'CACHE_LOCATION', 'IMAGE_SIZE':
        key = 'FLICKR_REST_%s' % suffix
        Flickr.SETTINGS[key] = pelican.settings[key]


class Flickr(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'title': directives.unchanged,
                   'alt': directives.unchanged,
                   'class': directives.unchanged,
                   'figclass': directives.unchanged,
                   'size': directives.unchanged,
                   }
    has_content = True
    generator = None

    def run(self):
        """Include a file as part of the content of this reST file."""

        flickr_id = self.arguments[0]

        figure_node = nodes.figure()
        div_node = htmlnodes.div()
        div_node['class'] = 'figure-container'
        target = htmlnodes.a()
        img_node = htmlnodes.img()
        caption = None

        for element in 'alt', 'title':
            if element in self.options:
                img_node[element] = self.options[element]

        if 'scale' in self.options:
            img_node['width'] = '%d%%' % self.options['scale']

        if 'class' in self.options:
            div_node['class'] = self.options['class']

        if 'figclass' in self.options:
            figure_node['class'] = self.options['figclass']

        if self.content:
            node = nodes.Element()          # anonymous container for parsing
            self.state.nested_parse(self.content, self.content_offset, node)
            first_node = node[0]

            if isinstance(first_node, nodes.paragraph):
                caption = htmlnodes.figcaption(first_node.rawsource, '',
                                               *first_node.children)
                caption.source = first_node.source
                caption.line = first_node.line
            elif not (isinstance(first_node, nodes.comment)
                      and len(first_node) == 0):
                error = self.state_machine.reporter.error(
                      'Figure caption must be a paragraph or empty comment.',
                      nodes.literal_block(self.block_text, self.block_text),
                      line=self.lineno)
                return [figure_node, error]
            if len(node) > 1:
                caption = nodes.legend('', *node[1:])

        if self.SETTINGS['api_client'] is None:
            logger.error('[flickreST]: Unable to get the Flickr API object.')
            target += img_node
            figure_node += target
            figure_node += caption
            div_node += figure_node
            # Return the placehorder for the image.
            return [nodes.raw('', div_node, format='html')]

        if 'size' in self.options:
            self.SETTINGS['FLICKR_REST_IMAGE_SIZE'] = self.options['size']

        info = flickradapter.get_photo(flickr_id, self.SETTINGS)

        if info:
            img_node['src'] = info['source_url']
            target['href'] = info['url']

            if 'alt' in img_node and not img_node['alt']:
                img_node['alt'] = info['title']
            if 'title' in img_node and not img_node['title']:
                img_node['title'] = img_node['title'] or info['title']

        target += img_node
        figure_node += target
        figure_node += caption
        div_node += figure_node

        return [nodes.raw('', div_node, format='html')]


def register():
    signals.initialized.connect(setup_settings)
    directives.register_directive('flickr', Flickr)
