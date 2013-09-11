keiko
=====

.. image:: https://badge.fury.io/py/keiko.png
    :target: http://badge.fury.io/py/keiko

.. image:: https://travis-ci.org/lanius/keiko.png
    :target: https://travis-ci.org/lanius/keiko

.. image:: https://coveralls.io/repos/lanius/keiko/badge.png
    :target: https://coveralls.io/r/lanius/keiko

keiko is Python and Web API clients for `Keiko-chan`_.


Installation
------------

keiko can be installed via pip or easy_install:

.. code-block:: bash

    $ pip install keiko

Or:

.. code-block:: bash

    $ easy_install keiko


Usage
-----

Firstly, setup Keiko-chan and assign IP address.

Python
~~~~~~

Specify the address of Keiko-chan and instantiate the client:

.. code-block:: python

    >>> import keiko
    >>> address = '192.168.1.2'  # example address of Keiko-chan
    >>> client = keiko.Client(address)

Control the lamps:

.. code-block:: python

    >>> client.lamps.green.on()  # turns on the lamp
    >>> client.lamps.green.status
    'on'
    >>> client.lamps.green.off()  # turns off the lamp
    >>> client.lamps.green.status
    'off'
    >>> client.lamps.yellow.blink()  # blinks the lamp
    >>> client.lamps.yellow.status
    'blink'
    >>> client.lamps.red.quickblink()  # blinks the lamp quickly
    >>> client.lamps.red.status
    'quickblink'
    >>> client.lamps.off()  # turns off the all lamps

With delay and duration time:

.. code-block:: python

    >>> client.lamps.red.on(wait=2, time=4)  # wait 2 second, light 2 seconds

Control the buzzer:

.. code-block:: python

    >>> client.buzzer.on()  # turns on the buzzer
    >>> client.buzzer.status
    'continuous'
    >>> client.buzzer.off()  # turns off the buzzer
    >>> client.buzzer.status
    'off'

Control the direct inputs and outputs:

.. code-block:: python

    >>> client.di.status
    {1: 'off', 2: 'off', 3: 'off', 4: 'off'}
    >>> client.do.status
    {1: 'off', 2: 'off', 3: 'off', 4: 'off'}
    >>> client.do(2).on()
    >>> client.do(2).status
    'on'
    >>> client.do.status
    {1: 'off', 2: 'on', 3: 'off', 4: 'off'}

Control the voices:

.. code-block:: python

    >>> client.voices.status
    'stop'
    >>> client.voices(1).play()  # plays #1 voice 
    >>> client.voices.stop()  # stops the voice 
    >>> client.voices(5).play(3)  # plays #5 voice 3 times
    >>> client.voices.stop()
    >>> client.voices(10).repeat()  # plays #10 voice repeatedly
    >>> client.voices.stop()

Web API
~~~~~~~

Specify the address of Keiko-chan and run Web API server:

.. code-block:: bash

    $ keiko 192.168.1.2
     * Running on http://127.0.0.1:8080/

Pass optional parameters to the server:

.. code-block:: bash

    $ keiko 192.168.1.2 --server myhost:5000
     * Running on http://myhost:5000/

Control the lamps:

.. code-block:: bash

    $ curl http://127.0.0.1:8080/lamps
    {
      "lamps": {
        "green": "off", 
        "red": "off", 
        "yellow": "off"
      }
    }

    $ curl http://127.0.0.1:8080/lamps/green/on
    {
      "result": "success"
    }

    $ curl http://127.0.0.1:8080/lamps/green
    {
      "lamps": {
        "green": "on"
      }
    }

With delay and duration time:

.. code-block:: bash

    $ curl http://127.0.0.1:8080/lamps/yellow/on?wait=2&time=4
    {
      "result": "success"
    }

Control the buzzer:

.. code-block:: bash

    $ curl http://127.0.0.1:8080/buzzer
    {
      "buzzer": "off"
    }

    $ curl http://127.0.0.1:8080/buzzer/on
    {
      "result": "success"
    }

Control the direct inputs and outputs:

.. code-block:: bash

    $ curl http://127.0.0.1:8080/di
    {
      "di": {
        "1": "off", 
        "2": "off", 
        "3": "off", 
        "4": "off"
      }
    }

    $ curl http://127.0.0.1:8080/do
    {
      "do": {
        "1": "off", 
        "2": "off", 
        "3": "off", 
        "4": "off"
      }
    }

    $ curl http://127.0.0.1:8080/do/2/on
    {
      "result": "success"
    }

Control the voices:

.. code-block:: bash

    $ curl http://127.0.0.1:8080/voices
    {
      "voices": "stop"
    }

    $ curl http://127.0.0.1:8080/voices/10/play
    {
      "result": "success"
    }


Caveats
-------

This module is unofficial and tested with only Keiko-chan 4G+ (DN-1510GL) yet. For more details, see `the official documentation`_.


.. _Keiko-chan: http://%e8%ad%a6%e5%ad%90%e3%81%a1%e3%82%83%e3%82%93.com/
.. _the official documentation: http://www.isa-j.co.jp/dn1510gl/files/dn1510gl-manual-20130426.pdf
