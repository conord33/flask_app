from datetime import datetime
from flask.ext.mongokit import Document

import dateutil.parser
import hashlib

# Data model
class Data(Document):
    __collection__ = 'data'
    structure = {
        'uid': unicode,
        'date': datetime,
        'date_strg': unicode,
        'name': unicode,
        'md5checksum': unicode
    }
    required_fields = ['uid', 'date', 'name', 'md5checksum']
    use_dot_notation = True

    def init(self, uid, name, date, md5checksum):
        self.date_strg = date
    	self.date = dateutil.parser.parse(date)
    	self.name = name
    	self.uid = uid
    	self.md5checksum = md5checksum

    # Determines if a data object is valid based on its md5checksum
    def is_valid(self):
    	return self.md5checksum == self.generate_sum()

    # Generates the md5checksum
    def generate_sum(self):
        strg = '{"date": "%s", "uid": "%s", "name": "%s"}' % (self.date_strg, self.uid, self.name)
        return hashlib.md5(strg).hexdigest()
