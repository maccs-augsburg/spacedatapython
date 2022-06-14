'''
Found this on youtube, will have to find the link.

import cProfile, pstats, io

To use this function, put the @profile decorator above the function you want to test

example: 
    @profile
    def count():
        .........
        .........
'''

import cProfile, pstats, io

def profile(fnc):
    '''A decorator that uses cProfile to profile a function'''
    '''Adapted from the Python 3.6 Docs: https://docs.python.org/3/library/profile.html#profile.Profile'''
    def inner(*args, **kwargs):

        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = "cumulative"
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner
