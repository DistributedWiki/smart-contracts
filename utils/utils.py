import hashlib
import jsonpickle


class JSONSerializable(object):

    def serialize(self):
        return jsonpickle.encode(self)

    def hash(self):
        return hashlib.sha256(self.serialize().encode()).hexdigest()

    @staticmethod
    def deserialize(data):
        return jsonpickle.decode(data)

# TODO - jsonpickle - is format consistent (e.g. between versions)
# TODO - another serialization method (preferably binary - pickle is not suitable as binary format may differ)
