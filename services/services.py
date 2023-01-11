from bson.objectid import ObjectId

class BaseMode:

    def select_param(self,extra_param):
        extra_param = [{param[0:param.find('.')]:{"$"+param[param.find('.') + 1:len(param)]:extra_param[param]}} if param.find('.') != -1 else {param: extra_param[param]}for param in extra_param]
        extra_param = {"$and": extra_param} if extra_param else {}
        return extra_param

    @property
    def json(self):
        return {k: v for k, v in self.__dict__.items() if v is not None and k not in ['data'] and not k.startswith('_')}

    @classmethod
    def save(self, db, data: json):
        return db.users.insert_one(data)

    @classmethod
    def update(self, db, id: str, data: dict):
        return db.users.update_many({"_id": ObjectId(id)}, {"$set": data})

    @classmethod
    def delete(self, db, id: str):
        return db.users.delete_one({"_id": ObjectId(id)})

    @classmethod
    def get_all(self, db, extra_param: list = []):
        extra_param = self.select_param(self,extra_param)
        return db.users.find(extra_param)

    @classmethod
    def get_by_id(self, db, id: str):
        return db.users.find_one({"_id":ObjectId(id)})

    @classmethod
    def simple_filter(self, **kwargs):
        return self.find_one(**kwargs)