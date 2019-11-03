class Printable:
    def __repr__(self):
        return "<" + type(self).__name__ + "> " + str(self.__dict__)
