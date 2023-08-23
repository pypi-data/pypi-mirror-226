.. highlight:: shell

============
Installation
============


Stable release
--------------

To install pylexique, run this command in your terminal:

.. code-block:: console

    $ pip install pylexique

This is the preferred method to install pylexique, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

You can also install pylexique by using Anaconda_ or Miniconda_ instead of `pip`_ .

To install Anaconda_ or Miniconda_, please follow the installation instructions on their respective websites.
After having installed Anaconda_ or Miniconda_, run these commands in your terminal:

.. code-block:: console

    $ conda config --add channels conda-forge
    $ conda config --set channel_priority strict
    $ conda install pylexique

If you already have Anaconda_ or Miniconda_ available on your system, just type this in your terminal:

.. code-block:: console

    $ conda install -c conda-forge pylexique
.. warning::
    If you intend to install pylexique on a Apple Macbook with an Apple M1 processor,
    it is advised that you install pylexique by using the conda installation method as all dependencies will be pre-compiled.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
.. _Anaconda: https://www.anaconda.com/products/individual
.. _Miniconda: https://docs.conda.io/en/latest/miniconda.html


From sources
------------

The sources for pylexique can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/SekouDiaoNlp/pylexique

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/SekouDiaoNlp/pylexique/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/SekouDiaoNlp/pylexique
.. _tarball: https://github.com/SekouDiaoNlp/pylexique/tarball/master
