#! /usr/bin/python
#-*- coding:utf-8 -*-
import tornado.web
from tornado import gen

def delist_arguments(args) -> dict:
    """
    Takes a dictionary, 'args' and de-lists any single-item lists then
    returns the resulting dictionary.

    In other words, {'foo': ['bar']} would become {'foo': 'bar'}
    """
    for arg, value in args.items():
        if len(value) == 1:
            args[arg] = value[0]
    return args

class MethodDispatcher(tornado.web.RequestHandler):

    def __dispatch(self):
        args = None

        if self.request.arguments:
            args = delist_arguments(self.request.arguments)


        if self.request.uri.endswith('/'):
            func = getattr(self, 'index', None)

            if args:
                return func(**args)
            else:
                return func()

        path = self.request.uri.split('?')[0]
        method = path.split('/')[-1]
        if not method.startswith('_'):
            func = getattr(self, method, None)
            if func:
                if args:
                    return func(**args)
                else:
                    return func()
            else:
                raise tornado.web.HTTPError(404)
        else:
            raise tornado.web.HTTPError(404)
    
    @gen.coroutine
    def get(self):
        """Returns self._dispatch()"""
        return self.__dispatch()
    
    @gen.coroutine
    def post(self):
        """Returns self._dispatch()"""
        return self.__dispatch()