class Service(object):
    def handle(self, source, message):
        for i in self.list_handlers():
            if type(self).can_handle(i, message):
                type(self).run(i, source, message)
    def list_handlers(self):
        for k in dir(self):
            v = getattr(self, k)
            if type(self).is_handler(v):
                yield v
    def find_handler(self, name):
        for handler in self.list_handlers():
            if type(self).tag(handler) == name:
                return handler
    def patch(self, ircclient):
        """
        Patches the ircclient to be more usable for clients of the service.

        Override this to change patching behavior.
        """
        pass
    @classmethod
    def is_handler(cls, func):
        """
        Override this method when subclassing.

        This method should return whether func is a service.
        """
        pass
    @classmethod
    def can_handle(cls, service, message):
        """
        Override this method when subclassing.

        This method should return whether the passed service can handle the
        given message.
        """
        pass
    @classmethod
    def handler(cls, tag):
        """
        Override this method when subclassing.

        This method should act as a decorator taking this form:
        @[Service].handler(tag)
        def handling_func([args]):

        converting a function to a handler of tag.
        """
        pass
    @classmethod
    def run(cls, handler, source, message):
        """
        Optionally override this method when subclassing.

        This method takes the handler function, the source, and the message,
        and somehow combines the three. The default behavior is to call the
        handler function on the source and the message.
        """
        return handler(source, message)
    @classmethod
    def tag(cls, service):
        """
        Override this method when subclassing.

        This method should return the tag of the passed service.
        """
        pass
