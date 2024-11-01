from __future__ import with_statement
from fabric.api import *
import fabric.contrib.files
import cStringIO as StringIO
import os
import re
import sys
import shlex
import urllib2
import commands
import subprocess

this_directory = os.path.dirname(os.path.abspath(__file__))

packages = ['',  # For the root 'tng' directory
            ]

extra_unittests = [os.path.join('../camelot', 'contrib', 'grapher'),
                   os.path.join('../camelot', 'contrib', 'powermanager')]

coverage_options = dict(NOSE_WITH_XUNIT='1',
                        NOSE_WITH_COVERAGE='1',
                        NOSE_WITH_COVER_PACKAGE='camelot-og')
coverage_tool = 'coverage'

if sys.platform.startswith('win'):
    fab = '{}\\Scripts\\fab.exe'.format(sys.exec_prefix)
    pip = '{}\\Scripts\\pip.exe'.format(sys.exec_prefix)
    nosetests = '{}\\Scripts\\nosetests.exe'.format(sys.exec_prefix)
    if not os.path.exists(nosetests):
        nosetests = '{0}\python.exe {0}\\Scripts\\nosetests'.format(
            sys.exec_prefix)
    trial = nosetests
else:
    fab = 'fab'
    # FIXME: on Fedora, pip is pip-python
    pip = 'pip'
    nosetests = 'nosetests'
    trial = 'trial'

test_runner = nosetests


def cleanpyc():
    print 'Number of .pyc files we found was: %s' % local(
        'find . -iname \'*.pyc\' | wc -l')
    local('find . -iname \'*.pyc\' -delete', capture=False)
    local("find . -name 'tnglogs' -prune -exec rm -r '{}' \;", capture=False)
    local("find . -name '_trial_temp' -prune -exec rm -r '{}' \;",
          capture=False)


def cleanboring():
    print "Number of ~ files we found was: %s" % local(
        'find . -iname \'*~\' | wc -l')
    local('find . -iname \'*~\' -delete', capture=False)


def install():
    local('%s install -e .' % pip, capture=False)


def distclean():
    '''Intended to clean up artefacts from installing TNG as root'''
    blacklist = ['doc/htmldoc/_build',
                 'examples',
                 'dist',
                 'build',
                 'Camelot_pi.egg-info',
                 'TODO',
                 'DEV_INSTALL']
    with cd(os.getcwd()):
        for item in blacklist:
            local('sudo rm -rf %s' % item)

'''
def pdf():
    usage_folder = os.path.join(this_directory, 'docs', 'usage')
    status, output = commands.getstatusoutput(
        'cd %s; pdflatex usage.tex' % usage_folder)
    if status != 0
        print "===LATEX COMPILE FAILED===\n%s" % output
        return
    else:
        print "PDF Created: %s/usage.pdf" % usage_folder
'''


def htmldoc():
    sphinx_dir = os.path.join(this_directory, 'doc', 'htmldoc')
    local('cd %s; make html' % sphinx_dir, capture=False)
    link = "file://" + os.path.join(sphinx_dir, '_build', 'html', 'index.html')
    print "Sphinx doc created: %s" % link


def cleanhtmldoc():
    sphinx_dir = os.path.join(this_directory, 'doc', 'htmldoc')
    local('cd %s; make clean' % sphinx_dir, capture=False)


def test(coverage=False, extra_opts=''):
    # Note: the unit and integration tests cannot currently be run in one
    # nosetests call as the unit tests interfere with the integration tests
    # causing them to fail, for example mock devices are left in the
    # backendservice.
    env = dict(os.environ)
    if coverage:
        env.update(coverage_options)
    cmd_line = '%s test %s' % (test_runner, extra_opts)
    p = subprocess.Popen(shlex.split(cmd_line),
                         cwd=this_directory,
                         env=env)
    ec = p.wait()
    if ec != 0:
        raise Exception('TESTS FAILED')


def ptest():
    test(extra_opts='--processes=10')


def coverage():
    with cd(this_directory):
        local('rm -f .coverage')
        local('rm -rf htmlcov')
        local('rm -f coverage.xml')
    # bug 128703 - only last run produces coverage stats
    test(coverage=True)
    local("%s html -i --include='tng*'" % coverage_tool)
    local("%s xml -i --include='tng*'" % coverage_tool)

    print 'Coverage stats output to file://%s' % os.path.join(
        this_directory, 'htmlcov', 'index.html')


def publish(server_url='http://pypi.cisco.com/'):
    local('python setup.py register -r "{server_url}" sdist upload '
          '-r "{server_url}"'.format(server_url=server_url))
