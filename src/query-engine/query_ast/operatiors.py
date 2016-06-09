# TODO Needs redesign
class Operator:
    '''
    Base operator class.
    '''

    def __init__(self, op, processor, operands=0):
        self.operation = op
        self.priority = priority
        self.processor = processor
        self.operands = operands

    def execute(*args):
        '''
        Pass the required number of operands to the
            operator
        '''
        return self.processor(*args)

class Equals(Operator):

    """Defines operator ="""

    def __init__(self, op, processor, operands):
        """TODO: to be defined1.

        Args:
            op (TODO): TODO
            processor (TODO): TODO
            operands (TODO): TODO


        """
        Operator.__init__(self)

        self._op = op
        self._processor = processor
        self._operands = operands
        
