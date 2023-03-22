
class BaseResource(object):

    def __init__(self, db_manager=None):
        self.db = db_manager