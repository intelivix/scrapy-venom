.. _intro-definition:

======================================
Overview
======================================

`Scrapy <http://doc.scrapy.org/>`_ is a fantastic tool to deal with data scraping. Although, for someone who doesn't work frequently with the framework, it might be hard to learn how to build some patterns which are common in scraping activities such as: "login", "search", "pagination", etc. Even more, it's hard to find some features like database pipelines, advanced middlewares and commands to run scripts. 

Scrapy-venom comes to fill the lack of libraries about these activities. It brings a new convention for the implementation of spiders, a more "dry" (Don't Repeat Yourself) and feature based way to program.

Venom classes are intended to solve simple scraping problems, once at time. It comes with a series of featured mixins which we call "steps". A set of "steps" build the spider "flow". They make the scraping programming more easy to read and understand.


Flow and Steps
---------------

Basically, the concept is a sequence of steps. The spider defines the initial step and every step will decide the next step to be executed. See the example:


**GoogleSpiderFlow**

The goal of this spider is make a query to google and get all links from the result.

* **STEP 1:** Make a GET request: https://www.google.com.br?q=keyword
* **STEP 2:** Get all links from the response.


.. code-block:: python
    

    # google-spider/spiders.py
    from scrapy_venom import spiders


    class GoogleSpider(spiders.SpiderFlow):

        name = 'google-spider'
        initial_step = 'example.SearchStep'



.. code-block:: python

    # google-spider/steps.py
    from scrapy_venom import steps
    from scrapy_venom.steps import generics


    class SearchStep(generics.SearchStep):

        search_url = 'http://www.google.com'
        next_step = 'example.LinkStep'

        def get_payload(self):
            return {
                'q': 'social+networks'
            }


    class LinkStep(steps.ItemStep):

        def clean_item(self, extraction):
            return {'url': extraction}

        def crawl(self, selector):
            yield selector.xpath('//a/@href')
