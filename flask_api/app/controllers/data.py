from flask import Blueprint, jsonify, request
from app.models import db

import datetime
import dateutil.parser
import app.helpers as helpers

mod_data = Blueprint('data', __name__, url_prefix='/data')

# Add data to mongo as a batch. It is added as all or nothing.
@mod_data.route("/batch", methods=["POST"])
def post_data():
    try:
        # Create list data objects
        dataList = [];
        for dataObj in request.json:
            # Create data object
            data = db.Data()
            data.init(dataObj['uid'], dataObj['name'], dataObj['date'], dataObj['md5checksum'])
            # Return error if the checksum is invalid
            if not data.is_valid():
                return helpers.make_error(400, 1004, "Invalid checksum.")
            # Add valid data to list
            dataList.append(data)

        # Only write to mongo if all data are valid
        for data in dataList:
            data.save();

        return '', 201

    # Handle invalid request, a different validation strategy would be more optimal
    except:
        return helpers.make_error(400, 1000, "Invalid json.")

# Count the data based on the date and uid provided
@mod_data.route('/count', methods=['GET'])
def get_data_count():
    # Get the query params
    date = request.args.get('date')
    uid = request.args.get('uid')

    # Make sure the necessary params are present
    if not uid or not date:
        return helpers.make_error(400, 1003, "A uid and a date are required")

    # Convert the date into a datetime with no time
    date = dateutil.parser.parse(date)
    date = datetime.datetime.combine(date, datetime.time.min)

    # Query mongo for given date and uid
    results = db.Data.find({
        "date": {
            "$gte": date,
            "$lt": date + datetime.timedelta(days=1)
        },
        "uid": uid
    })

    # Count the results
    count = 0
    for result in results:
        count += 1

    return jsonify({"count": count})

