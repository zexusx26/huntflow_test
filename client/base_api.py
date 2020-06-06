from .requester import Requester


class BaseAPIClass:
    """ Базовый класс для методов АПИ клиента. """

    def __init__(self, requester: Requester):
        """ Инициализация базового класса методов АПИ клиента.

        :param requester: экземпляр класса-обертки requests
        :type requester: Requester
        """
        self.requester = requester
