Olchiki
======

|Build Status| |Version| |Python| |Size| |Codecov|

Olchiki is a package for Olchiki language users with various functionalities including Olchiki date and Olchiki numeric conversation.

It can be used to get Olchiki date that includes year, month, date, weekday and season of Olchiki year.
Olchiki has used the rules from Wikipedia https://en.wikipedia.org/wiki/Bengali_calendars to convert 
Gregorian date to Olchiki date. It is based on the revised version of the Bengali calendar which was officially adopted in Olchikidesh in 1987.
Among the Bengali community in India, the provided date may differ.

Moreover, this package has also a method to convert English numeric string to Olchiki numeric string.

This software can be used on Linux/Unix, Mac OS and Windows systems.

Features
~~~~~~~~

-  Get Olchiki date that includes:

   - Olchiki Date (১-৩১)

   - Olchiki Month ("বৈশাখ", "জ্যৈষ্ঠ", "আষাঢ়", "শ্রাবণ", "ভাদ্র", "আশ্বিন", "কার্তিক", "অগ্রহায়ণ", "পৌষ", "মাঘ", "ফাল্গুন", "চৈত্র")

   - Olchiki Year (১৯৮৭ - )

   - Olchiki Season ("গ্রীষ্ম", "বর্ষা", "শরৎ", "হেমন্ত", "শীত", "বসন্ত")

   - Olchiki Weekday ("শনিবার", "রবিবার", "সোমবার", "মঙ্গলবার", "বুধবার", "বৃহস্পতিবার", "শুক্রবার")

-  Convert English numeric string to Olchiki numeric string (123456 -> ১২৩৪৫৬).

Installation
~~~~~~~~~~~~

We recommend install ``olchiki`` through pip install using Python 3.

.. code:: bash

    $ pip install olchiki

Example
~~~~~~~

To get today's date in Olchiki calendar:

.. code:: python

	import olchiki
	olchiki_date = olchiki.get_date()
	print(olchiki_date) 
	# Output: {'date': '৮', 'month': 'আষাঢ়', 'year': '১৪২৪', 'season': 'বর্ষা', 'weekday': 'বৃহস্পতিবার'} 

	
To convert any Gregorian date to Olchiki date :

.. code:: python

    import olchiki
    olchiki_date = olchiki.get_date(20,6,2017) # date, month, year
    print(olchiki_date) 
    # Output: {'date': '৬', 'month': 'আষাঢ়', 'year': '১৪২৪', 'season': 'বর্ষা', 'weekday': 'মঙ্গলবার'}
	
To convert any English numeric string to Olchiki numeric string :

.. code:: python

    import olchiki
    olchiki_numeric_string = olchiki.convert_english_digit_to_olchiki_digit("123456")
    print(olchiki_numeric_string)
    # Output: ১২৩৪৫৬
	
Contribute
~~~~~~~~~~

Create Github Pull Request https://github.com/arsho/olchiki/pulls

If you have suggestion use GitHub issue system or send a message in Facebook https://www.facebook.com/ars.shovon.

Thanks
~~~~~~

Influenced by বঙ্গাব্দ - jQuery Plugin 
https://github.com/nuhil/olchiki-calendar

.. |Build Status| image:: https://travis-ci.org/arsho/olchiki.svg?branch=master
   :target: https://travis-ci.org/arsho/olchiki

.. |Version| image:: https://img.shields.io/pypi/v/olchiki.svg?
   :target: http://badge.fury.io/py/olchiki
   
.. |Python| image:: https://img.shields.io/pypi/pyversions/olchiki.svg?
   :target: https://pypi.python.org/pypi/olchiki/0.0.1
      
.. |Size| image:: https://img.shields.io/github/size/arsho/olchiki/olchiki/__init__.py.svg?
   :target: https://github.com/arsho/olchiki/   
   
.. |Codecov| image:: https://codecov.io/github/arsho/olchiki/coverage.svg?branch=master
   :target: https://codecov.io/github/arsho/olchiki      