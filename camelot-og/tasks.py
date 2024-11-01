from __future__ import print_function
import os
import sys
import shlex
import subprocess
import functools

from invoke import run, task
import invoke.runners
import invoke.exceptions
from blessings import Terminal

if sys.version_info.major == 2:
    from base64 import encodestring as encodebytes
else:
    from base64 import encodebytes


terminal = Terminal()

this_directory = os.path.dirname(os.path.abspath(__file__))

packages = ['',  # For the root 'tng' directory
            ]

extra_unittests = [os.path.join('../camelot', 'contrib', 'grapher'),
                   os.path.join('../camelot', 'contrib', 'powermanager')]

coverage_options = dict(NOSE_WITH_XUNIT='1',
                        NOSE_WITH_COVERAGE='1',
                        NOSE_WITH_COVER_PACKAGE='camelot-og')
coverage_tool = 'coverage'

os.environ['LC_ALL'] = 'en_US.UTF-8'

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

def command(command):
    run(command, echo=True)


def command_output(command):
    result = run(command, echo=False, hide=True)
    return result.stdout


def return_capturer(func, dest):
    '''
    Returns a callable which runs func and captures the return value or
    exception in dest.
    '''
    @functools.wraps(func)
    def worker(*a, **k):
        dest[func] = func(*a, **k)
    return worker


def quit(code):
    ' Fail hard with a custom exit code '
    # There doesn't seem to be a sane way of failing a task?
    raise invoke.exceptions.Failure(
        invoke.runners.Result(
            exited=code,
            # only supplying these to satisfy the Result constructor
            command=None,
            stdout=None,
            shell=None,
            env=None,
            stderr=None,
            pty=None))


@task
def cleanpyc(ctx):
    print(terminal.bold_yellow('Cleaning pyc files (and others)'))
    print('Number of .pyc files we found was: %s' % command_output(
        "find . -iname '*.pyc' | wc -l").rstrip())
    command("find . -iname '*.pyc' -delete")
    command("find . -type d -name '__pycache__' -prune -exec rm -r '{}' \;")
    command("find . -type d -name 'tnglogs' -prune -exec rm -r '{}' \;")
    command("find . -type d -name '_trial_temp' -prune -exec rm -r '{}' \;")


@task
def cleanboring(ctx):
    print("Number of ~ files we found was: %s" % command_output(
        "find . -iname '*~' | wc -l"))
    command("find . -iname '*~' -delete")


@task
def install(ctx, extras=None, quiet=False):
    target = '.'
    pip_args = []
    if extras:
        target = '{}[{}]'.format(target, extras)
    if quiet:
        pip_args += ['--quiet']

    cmd = ' '.join([pip, 'install'] + pip_args + ['--editable', target])
    command(cmd)


@task
def distclean(ctx):
    '''Intended to clean up artefacts from installing TNG as root'''
    blacklist = ['doc/htmldoc/_build',
                 'examples',
                 'dist',
                 'build',
                 'Camelot_pi.egg-info',
                 'TODO',
                 'DEV_INSTALL']
    for item in blacklist:
        command('sudo rm -rf %s' % item)


@task
def htmldoc(ctx):
    sphinx_dir = os.path.join(this_directory, 'doc', 'htmldoc')
    command('cd %s; make html' % sphinx_dir)
    link = "file://" + os.path.join(sphinx_dir, '_build', 'html', 'index.html')
    print("Sphinx doc created: %s" % link)


@task
def cleanhtmldoc(ctx):
    sphinx_dir = os.path.join(this_directory, 'doc', 'htmldoc')
    command('cd %s; make clean' % sphinx_dir)

@task
def test(ctx, coverage=False, extra_opts=''):
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
