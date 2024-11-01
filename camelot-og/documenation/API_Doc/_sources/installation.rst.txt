************
Installation
************

For the keen amongst you, the install process basically consists of checking out the latest source from `gitorious <https://bitbucket-eng-gpk1.cisco.com/bitbucket/projects/CAMELOTPI/repos/camelot-pi>`_ and installing using pip.
We officially support all platforms.


Any Platform
============
Prerequisites
-------------

* Ubuntu 12.04 or above / centos 7 or above
* Python 2.7 or above
* git
* Supported Camelot build: `Download <http://wwwin-vts.cisco.com/camelot/>`
* pip

Installation generic
--------------------
These commands will get you up-and-running with Camelot-pi right away::

    cd ~
    git clone ssh://git@bitbucket-eng-gpk1.cisco.com:7999/camelotpi/camelot-pi.git camelot-pi
    cd camelot-pi
    sudo ./INSTALL

Installation with virtualenv
----------------------------
These commands will get you up-and-running with python2.X or python3.X versions of camelot-pi right away::

    sudo pip install virtualenv
    # assuming python3 has been already installed, and binary exists in /usr/bin/python3.7
    # donot use sudo for any of the below commands
    virtualenv -v --python=/usr/bin/python3.7 ~/camelot-pi-virtualenv
    source ~/camelot-pi-virtualenv/bin/activate
    cd ~
    git clone ssh://git@bitbucket-eng-gpk1.cisco.com:7999/camelotpi/camelot-pi.git camelot-pi
    cd camelot-pi
    ./INSTALL

.. note::
    * You need to have an activated `bitbucket <https://bitbucket-eng-gpk1.cisco.com>`_ account to be able to check out Camelot-pi
    * For a new bitbucket account, click on "open a case" tab in `bitbucket <https://bitbucket-eng-gpk1.cisco.com>`_ and raise a case.
    * Last command should be executed as super user
    * Expected that you have a TNGpi installation up and running in the machine, in case of using with TNGpi
    * Do not use SUDO with virtualenv commands.
    * Recommendation is always to use virtualenv, so that OS dependent python does not get corrupted.

* This will download and install Camelot-pi's Python dependencies, and then install Camelot-pi itself.
