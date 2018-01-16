Flickrst
==========

Flickrst is a plugin for Pelican_ static site generator.
This plugins add a reStructuredText directive (`flickr`) to display
images available in Flickr_.


Installation
------------

To install the plugin, clone the this repository in a place where the
Pelican plugins live:

.. code-block:: bash

    $ git clone https://github.com/gpoo/flickrst.git

and add it in the plugin_ section of your blog configuration (likely,
`pelicanconf.py`.


.. code-block:: python

    PLUGINS = [
        # ...
        'flickrst',
        # ...
    ]


Usage
-----

In your articles, just add lines to your posts that look like:

.. code-block:: ReST

    .. flickr:: 31456067436
        :alt: A notebook with notes
        :title: Together, little bull and notes.
        :class: div-class
        :figclass: fig-class
        :size: Large

        Caption notes as written in a notebook.

The plugin will retrieve the Flickr image with id ``31456067436`` in the
text (page or article). The resulting HTML might look like:

.. code-block:: html

    <div class="div-class">
      <figure class="div-class">
        <a href="https://www.flickr.com/photos/gpoo/31456067436/">
        <img alt="A notebook with notes"
             src="https://farm1.staticflickr.com/598/31456067436_08ae67c21e_b.jpg"
             title="Together, little bull and notes."/></a>
        <figcaption>Caption notes as written in a notebook.</figcaption>
      </figure>
    </div>

The only mandatory data is the photo id. If you want to set the title
from the Flickr image as ``alt`` or ``title``, then you can leave empty
such property. For example:

    .. flickr:: 31456067436
        :alt: 

The result will be:

.. code-block:: html

    <div class="figure-container">
      <figure>
        <a href="https://www.flickr.com/photos/gpoo/31456067436/">
        <img alt="Together"
        src="https://farm1.staticflickr.com/598/31456067436_08ae67c21e_z.jpg"/></a>
      </figure>
    </div>


Settings
--------

``FLICKR_REST_CACHE_LOCATION`` - The cache location which stores the
looked up photo information. This dramatically speeds up building of
the site and permits you to do it offline as well. Defaults to
`/tmp/org.calcifer.flickrst-images.cache` (Optional)

``FLICKR_TAG_IMAGE_SIZE`` - The size alias used to retrieve the url
for photo. Default is 'Medium 640'. See the `Flickr getSizes documentation`_
for the valid values. (Optional)


Flickr Settings
---------------

The following two settings are required. In order to set them up,
you will need to set up a Flickr API key. You can do this by
`creating an app on Flickr`_. If the blog is a personal blog, then
apply for a non-commercial key. Once you've got your key and secret,
add them to your `Pelican configuration`_.

``FLICKR_API_KEY`` - The API key for your app to access the Flickr API.
(Required)

``FLICKR_API_SECRET`` - The API secret for your app to access the Flickr API.
(Required)


Flickr Tokens
-------------

A Flickr API token is only required if you want to access photos that are
private to your account and cannot be gotten through the public API. I'll
assume you know what you're doing and how to get a Flickr API token for
this setting.

``FLICKR_API_TOKEN`` - The API token to access the Flickr API. (Optional)


Notes
-----

This plugin was inspired by the `Pelican Flickr Tag`_ plugin, and it uses
similar settings (The settings' section is a copy its manual). I have
contributed to that plugin, and finally ended writing a new pluging. I
think a `ReST` directive makes the text cleaner, and it enables some
tinkering.

As `Pelican Flickr Tag`, this code also uses portions of code from
`flickrpy`_.


License
-------

Uses the `MIT`_ license.


.. _Pelican: http://blog.getpelican.com/
.. _Flickr: http://flickr.com/
.. _`Pelican configuration`: http://docs.getpelican.com/en/latest/settings.html
.. _`Pelican Flickr Tag`: https://github.com/streeter/pelican-flickrtag
.. _flickrpy: http://code.google.com/p/flickrpy
.. _MIT: http://opensource.org/licenses/MIT
.. _`creating an app on Flickr`: http://www.flickr.com/services/apps/create/apply/
.. _`Flickr getSizes documentation`: http://www.flickr.com/services/api/flickr.photos.getSizes.htm

