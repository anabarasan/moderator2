import logging
import webapp2

logger = logging.getLogger('WSGIApplication')


class WSGIApplication(webapp2.WSGIApplication):
    def __init__(self, *args, **kwargs):
        super(WSGIApplication, self).__init__(*args, **kwargs)
        self.router.set_dispatcher(self.__class__.custom_dispatcher)

    @staticmethod
    def custom_dispatcher(router, request, response):
        logger.debug(router.match_routes)
        logger.debug(router.build_routes)
        rv = router.default_dispatcher(request, response)
        if isinstance(rv, basestring):
            rv = webapp2.Response(rv)
        elif isinstance(rv, tuple):
            rv = webapp2.Response(*rv)
        return rv

    def route(self, url, name):
        def outer_wrapped(cls):
            logger.debug("Adding route %s to class %s with name %s"
                         % (url, cls, name))
            self.router.add(webapp2.Route(url, cls, name))
            return cls
        return outer_wrapped
