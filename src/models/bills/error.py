
class BillErrors(Exception):
    def __init__(self, message):
        self.message = message


class ReimbursementAmountNotAdded(BillErrors):
    pass

class NoBills(BillErrors):
    pass
