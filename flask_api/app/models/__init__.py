from flask.ext.mongokit import MongoKit

from .data import Data

# Register models to the database
db = MongoKit()
db.register([Data])