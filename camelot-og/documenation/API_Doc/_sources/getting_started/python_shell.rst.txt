************
Python Shell
************

Start Python shell::

    $ python


    >>> import camelot
    >>> camelot.get_compat_versions('10.1.2.56', 9988)
    {'CTMS': '1.1.0', 'CME': '9.1', 'CUCM': '9.0.0', 'VAPIEI': '9.5.0.0.15.8', 'CUP': '8.5'}
    >>> ep1 = camelot.create_new_endpoint('10.106.248.199', 5004, 'sipx', 'SEPBAACBAAC7001')
    >>> ep1
    <camelot.endpoint.CamelotEndpoint object at 0x29ed490>
    >>> ep2 = camelot.create_new_endpoint('10.106.248.199', 5004, 'sipx', 'SEPBAACBAAC7002')
    >>> ep2
    <camelot.endpoint.CamelotEndpoint object at 0x29ed491>
    >>> ep1.place_call('7002')
    >>> ep2.get_calls()
    [<camelot.response.Call at 0x39bc2d0>]
    
