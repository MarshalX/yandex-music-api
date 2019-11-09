import json

from abc import ABCMeta


class YandexMusicObject:
    __metaclass__ = ABCMeta
    _id_attrs = ()

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return str(self)

    def __getitem__(self, item):
        return self.__dict__[item]

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = data.copy()

        return data

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        def parse(val):
            if hasattr(val, 'to_dict'):
                return val.to_dict()
            elif isinstance(val, list):
                return [parse(it) for it in val]
            elif isinstance(val, dict):
                return {k: parse(v) for k, v in val.items()}
            else:
                return val

        data = self.__dict__.copy()
        data.pop('client', None)
        data.pop('_id_attrs', None)

        return parse(data)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._id_attrs == other._id_attrs
        return super(YandexMusicObject, self).__eq__(other)

    def __hash__(self):
        if self._id_attrs:
            frozen_attrs = tuple(frozenset(attr) if isinstance(attr, list) else attr for attr in self._id_attrs)
            return hash((self.__class__, frozen_attrs))
        return super(YandexMusicObject, self).__hash__()
