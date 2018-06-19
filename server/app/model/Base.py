# -*- coding: utf-8 -*-
import json
from playhouse.flask_utils import FlaskDB

db_wrapper = FlaskDB()

STATUS_VALID = 1
STATUS_INVALID = 0


class BaseModel(db_wrapper.Model):

    def __str__(self):
        r = {}
        for k in self._data.keys():
            try:
                r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        # return str(r)
        return json.dumps(r, ensure_ascii=False)
