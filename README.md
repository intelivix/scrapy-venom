# Scrapy-Venom


**Warning: we do not recomend using this package yet, we're working on it. Please, wait for more features.**

Overview
----------

[Scrapy](http://doc.scrapy.org/) is a fantastic tool to deal with data scraping. Although, for someone who doesn't work frequently with the framework, it might be hard to learn how to build some patterns which are common in scraping activities such as: "login", "search", "pagination", etc. Even more, it's hard to find some features like database pipelines, advanced middlewares and commands to run scripts. 

Scrapy-venom comes to fill the lack of libraries about these activities. It brings a new convention for the implementation of spiders, a more "dry" (Don't Repeat Yourself) and feature based way to program.

Venom classes are intended to solve simple scraping problems, once at time. It comes with a series of featured mixins which we call "steps". A set of "steps" build the spider "flow". They make the scraping programming more easy to read and understand.

The documentation is available at: http://scrapy-venom.readthedocs.org/en/latest/

Requirements
----------------
* Python 2.7
* Works on Linux, Windows, Mac OSX, BSD

Install
-------------

The quick way:

```bash
  $ pip install scrapy-venom
```

