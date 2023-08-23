tidalapi
========

.. image:: https://img.shields.io/pypi/v/tidalapi.svg
    :target: https://pypi.org/project/tidalapi

.. image:: https://api.netlify.com/api/v1/badges/f05c0752-4565-4940-90df-d2b3fe91c84b/deploy-status
    :target: https://tidalapi.netlify.com/

Unofficial Python API for TIDAL music streaming service.

Requires Python 3.9 or higher.

0.7.x Migration guide
---------------------
The 0.7.x rewrite is now complete, see the `migration guide <https://tidalapi.netlify.app/migration.html#migrating-from-0-6-x-0-7-x>`_ for dealing with it

Installation
------------

Install from `PyPI <https://pypi.python.org/pypi/tidalapi/>`_ using ``pip``:

.. code-block:: bash

    $ pip install tidalapi



Example usage
-------------

.. code-block:: python

    import tidalapi

    session = tidalapi.Session()
    # Will run until you visit the printed url and link your account
    session.login_oauth_simple()
    # Override the required playback quality, if necessary
    # Note: Set the quality according to your subscription.
    # Normal: Quality.low_320k
    # HiFi: Quality.high_lossless
    # HiFi+ Quality.hi_res_lossless
    session.audio_quality = Quality.low_320k

    album = session.album(66236918)
    tracks = album.tracks()
    for track in tracks:
        print(track.name)
        for artist in track.artists:
            print(' by: ', artist.name)


Documentation
-------------

Documentation is available at https://tidalapi.netlify.app/

Development
-----------

This project uses poetry for dependency management and packaging. To install dependencies and setup the project for development, run:

.. code-block:: bash
    
        $ pip install pipx
        $ pipx install poetry
        $ poetry install --no-root
