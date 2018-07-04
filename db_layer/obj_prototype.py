import datetime


class ObjPrototype:

    dbname = "General"
    collection = "GeneralObj"

    def __init__(self,**kwargs):
        self.obj = {}
        for key in kwargs:
            self.obj[key] = kwargs[key]

    def __iter__(self):
        for key in self.obj:
            yield key, self.obj[key]

    def __len__(self):
        return len(self.obj)

    def __str__(self):
        return self.obj.__repr__()

    def __call__(self, *args, **kwargs):
        if len(args) > 0 and args[0] in self.obj:
            return self.obj[args[0]]
        else:
            return self.obj


class Transaction(ObjPrototype):

    dbname = "Personal"
    collection = "Financial"

    def __init__(self, amount,timestamp,
                 tags,description="", id=""):
        super().__init__(amount=amount,timestamp=timestamp,
                         tags=tags,description=description)
        self.id = id

    def get_time(self):
        return datetime.datetime.fromtimestamp(self.obj["timestamp"])

    def __repr__(self):
        return "Time: {0}, Amount: ${1}, Tags: {2}, Description: {3}".\
                format(self.get_time().__repr__(),self.obj["amount"],
                       self.obj["tags"].__repr__(),self.obj["description"])

    def __str__(self):
        return self.__repr__()

    def __add__(self, other):
        if isinstance(other, Transaction) and self!=other:
            return Transaction(amount = self.obj["amount"]+other.obj["amount"],
                               timestamp = max(self.obj["timestamp"],other.obj["timestamp"]),
                               tags = self.obj["tags"].union(other.obj["tags"]),
                               description=self.obj["description"] + ";"+ other.obj["description"])

