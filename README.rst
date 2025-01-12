ratelimit |build| |maintainability|
===================================

APIs are a very common way to interact with web services. As the need to
consume data grows, so does the number of API calls necessary to remain up to
date with data sources. However many API providers constrain developers from
making too many API calls. This is know as rate limiting and in a worst case
scenario your application can be banned from making further API calls if it
abuses these limits.

This packages introduces a function decorator preventing a function from being
called more often than that allowed by the API provider. This should prevent
API providers from banning your applications by conforming to their rate
limits.

Installation
------------

PyPi
~~~~

Add this line to your application's requirements.txt:

.. code:: python

    ratelimit

And then execute:

.. code:: bash

    $ pip install -r requirements.txt

Or install it yourself:

.. code:: bash

    $ pip install ratelimit

GitHub
~~~~~~

Installing the latest version from Github:

.. code:: bash

    $ git clone https://github.com/tomasbasham/ratelimit
    $ cd ratelimit
    $ python setup.py install

Usage
-----

To use this package simply decorate any function that makes an API call:

.. code:: python

    from ratelimit import limits

    import requests

    FIFTEEN_MINUTES = 900

    @limits(calls=15, period=FIFTEEN_MINUTES)
    def call_api(url):
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception('API response: {}'.format(response.status_code))
        return response

This function will not be able to make more then 15 API call within a 15 minute
time period.

The arguments passed into the decorator describe the number of function
invocation allowed over a specified time period (in seconds). If no time period
is specified then it defaults to 15 minutes (the time window imposed by
Twitter).

If a decorated function is called more times than that allowed within the
specified time period then a ``ratelimit.RateLimitException`` is raised. This
may be used to implement a retry strategy such as an `expoential backoff
<https://pypi.org/project/backoff/>`_

.. code:: python

    from ratelimit import limits, RateLimitException
    from backoff import on_exception, expo

    import requests

    FIFTEEN_MINUTES = 900

    @on_exception(expo, RateLimitException, max_tries=8)
    @limits(calls=15, period=FIFTEEN_MINUTES)
    def call_api(url):
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception('API response: {}'.format(response.status_code))
        return response

Alternatively to cause the current thread to sleep until the specified time
period has ellapsed and then retry the function use the ``sleep_and_retry``
decorator. This ensures that every function invocation is successful at the
cost of halting the thread.

.. code:: python

    from ratelimit import limits, sleep_and_retry

    import requests

    FIFTEEN_MINUTES = 900

    @sleep_and_retry
    @limits(calls=15, period=FIFTEEN_MINUTES)
    def call_api(url):
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception('API response: {}'.format(response.status_code))
        return response

Additionally a collection of exception classes can be passed as an argument to
the constructor. If the wrapped function raises any of these exceptions they
will we wrapped in a ``ratelimit.RateLimitException``. This allows the usage
of the ``sleep_and_retry`` decorator functionality on arbitrary exceptions.

.. code:: python

    from ratelimit import limits, sleep_and_retry

    @sleep_and_retry
    @limits(calls=1, period=10, wrap_exceptions=(RuntimeError, IOError))
    def raise_exception():
        raise RuntimeError("Wrapped in RateLimitException")
        
License
-------

This project is licensed under the `MIT License <LICENSE.txt>`_.

.. |build| image:: https://travis-ci.com/tomasbasham/ratelimit.svg?branch=master
    :target: https://travis-ci.com/tomasbasham/ratelimit

.. |maintainability| image:: https://api.codeclimate.com/v1/badges/21dc7c529c35cd7ef732/maintainability
    :target: https://codeclimate.com/github/tomasbasham/ratelimit/maintainability
    :alt: Maintainability
