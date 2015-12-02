
#
# Enforcing types in python
# Copyright 2004 Justin Shaw 
# Taken from http://code.activestate.com/recipes/355638-type-checked-argument-lists-with-decorators/
#
# Distributed under the terms of the PSF LICENSE AGREEMENT
#
#

def require(*types):
    '''
    Return a decorator function that requires specified types.
    types -- tuple each element of which is a type or class or a tuple of
             several types or classes.
    Example to require a string then a numeric argument
    @require(str, (int, long, float))

    will do the trick
    '''
    def deco(func):
        '''
        Decorator function to be returned from require().  Returns a function
        wrapper that validates argument types.
        '''
        def wrapper (*args):
            '''
            Function wrapper that checks argument types.
            '''
            assert len(args) == len(types), 'Wrong number of arguments.'
            for a, t in zip(args, types):
                if type(t) == type(()):
                    # any of these types are ok
                    assert sum(isinstance(a, tp) for tp in t) > 0, '''\
%s is not a valid type.  Valid types:
%s
''' % (a, '\n'.join(str(x) for x in t))
                assert isinstance(a, t), '%s is not a %s type' % (a, t)
            return func(*args)
        return wrapper
    return deco