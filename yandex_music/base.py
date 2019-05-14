import json

from abc import ABCMeta


class YandexMusicObject(object):
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
        data = dict()
        for key, value in self.__dict__.items():
            if key in ('client',
                       '_id_attrs'):
                continue

            if hasattr(value, 'to_dict'):
                data[key] = value.to_dict()
            else:
                data[key] = value

        return data

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._id_attrs == other._id_attrs
        return super(YandexMusicObject, self).__eq__(other)

    def __hash__(self):
        if self._id_attrs:
            return hash((self.__class__, self._id_attrs))
        return super(YandexMusicObject, self).__hash__()
