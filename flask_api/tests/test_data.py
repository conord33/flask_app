from flask import json
from flask.ext.mongokit import Connection
from app import app

import helpers
import unittest
import dateutil.parser

class DataTestCase(unittest.TestCase):
    
    # Set up test app and add test cases to mongo
    def setUp(self):
        self.app = app.test_client()
        db_name = app.config['MONGODB_DATABASE']
        connection = Connection()
        connection[db_name].data.insert({
            'uid': '1',
            'name': 'John Doe',
            'date': dateutil.parser.parse('2015-05-12T14:36:00.451765'),
            'md5checksum': 'e8c83e232b64ce94fdd0e4539ad0d44f'
        })

        connection[db_name].data.insert({
            'uid': '2',
            'name': 'Sammy',
            'date': dateutil.parser.parse('2015-05-12T14:36:00.469965'),
            'md5checksum': '2563f143870ad4b20efc9588702cfc99'
        })

        connection[db_name].data.insert({
            'uid': '2',
            'name': 'John Doe',
            'date': dateutil.parser.parse('2015-05-12T14:36:00.451765'),
            'md5checksum': '33d2def3aae252ba7af85c2e5543d0c4'
        })

    # Clear out mongo after each test
    def tearDown(self):
        db_name = app.config['MONGODB_DATABASE']
        connection = Connection()
        connection[db_name].data.remove()

    # Test each error case for post data
    def test_post_data_bad_request(self):
        resp1 = self.app.post('/data/batch', content_type='application/json')
        helpers.assert_error(resp1, 400, 1000)

        resp2 = self.app.post('/data/batch', data=json.dumps({"json":"json"}))
        helpers.assert_error(resp2, 400, 1000)

        resp3 = self.app.post('/data/batch', data=json.dumps([{"jsosssn":"jsossssn"}]), content_type='application/json')
    	helpers.assert_error(resp3, 400, 1000)

    	resp1 = self.app.post('/data/batch', data=json.dumps([{"md5checksum":"jsossssn"}]), content_type='application/json')
    	helpers.assert_error(resp1, 400, 1000)

        data = [{
            "md5checksum":"jsossssn",
            "uid":"snarf",
            "name":"snarf",
            "date":"not a date"
        }]
        resp4 = self.app.post('/data/batch', data=json.dumps(data), content_type='application/json')
        helpers.assert_error(resp4, 400, 1000)

    # Test invalid checksums
    def test_post_data_bad_data(self):
    	data1 = [{
    		"md5checksum":"jsossssn",
    		"uid":"snarf",
    		"name":"snarf",
    		"date":"2015-05-12T14:36:00.451765"
    	}]
    	resp1 = self.app.post('/data/batch', data=json.dumps(data1), content_type='application/json')
    	helpers.assert_error(resp1, 400, 1004)

        # Once correct checksum one invalid one
    	data2 = [
    		{
	    	    'uid': '1',
	            'name': 'John Doe',
	            'date': '2015-05-12T14:36:00.451765',
	            'md5checksum': 'e8c83e232b64ce94fdd0e4539ad0d44f'
	        },
	        {
	    		"md5checksum":"jsossssn",
	    		"uid":"snarf",
	    		"name":"snarf",
	    		"date":"2015-05-12T14:36:00.451765"
	    	}
	    ]
    	resp2 = self.app.post('/data/batch', data=json.dumps(data2), content_type='application/json')
    	helpers.assert_error(resp2, 400, 1004)

    # Test functioning post data
    def test_post_data(self):
    	data = [{
    	    'uid': '1',
            'name': 'John Doe',
            'date': '2015-05-12T14:36:00.451765',
            'md5checksum': 'e8c83e232b64ce94fdd0e4539ad0d44f'
        }]
    	resp1 = self.app.post('/data/batch', data=json.dumps(data), content_type='application/json')
        assert resp1.status_code == 201
    	assert resp1.data == ''

        data = [
            {
                'uid': '2',
                'name': 'Sammy',
                'date': '2015-05-12T14:36:00.469965',
                'md5checksum': '2563f143870ad4b20efc9588702cfc99'
            },
            {
                'uid': '2',
                'name': 'John Doe',
                'date': '2015-05-12T14:36:00.451765',
                'md5checksum': '33d2def3aae252ba7af85c2e5543d0c4'
            }
        ]
        resp2 = self.app.post('/data/batch', data=json.dumps(data), content_type='application/json')
        assert resp2.status_code == 201
        assert resp2.data == ''

    # Test invalid request for get data count
    def test_get_data_count_bad_params(self):
    	resp1 = self.app.get('/data/count')
        helpers.assert_error(resp1, 400, 1003)

        resp2 = self.app.get('/data/count?date=2011-09-09')
        helpers.assert_error(resp2, 400, 1003)

        resp3 = self.app.get('/data/count?uid=4')
        helpers.assert_error(resp3, 400, 1003)

    # Test functioning counts based on data added to mongo in setup method
    def test_get_data_count(self):
        resp1 = self.app.get('/data/count?date=2015-05-11&uid=2')
        data = json.loads(resp1.data)
        assert resp1.status_code == 200
        assert data['count'] == 0

        resp2 = self.app.get('/data/count?date=2015-05-12&uid=2')
        data = json.loads(resp2.data)
        assert resp2.status_code == 200
        assert data['count'] == 2

        resp3 = self.app.get('/data/count?date=2015-05-12&uid=1')
        data = json.loads(resp3.data)
        assert resp3.status_code == 200
        assert data['count'] == 1

        resp1 = self.app.get('/data/count?date=2015-05-12&uid=3')
        data = json.loads(resp1.data)
        assert resp1.status_code == 200
        assert data['count'] == 0

