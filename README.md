# Flask API with NGINX, Ansible, uWSGI, MonogDB, and Supervisor

This is a very basic Flask API that demos how to setup an environment for a Flask application.  It comes with a vagrant setup that is provisioned with Ansible and should start the api on start up.

## Running the API

Runing `vagrant up` in the project directory should spin up a vagrant box
listening on `localhost:8080`.

### Running the tests

The tests can be run by taking the following steps.
1. ssh into the vagrant box   `vagrant ssh`
2. go into the app directory  `cd /srv/webapps/flask_api/src`
3. configure venv             `ssource ../venv/bin/activat`
4. run the tests              `python tests.py`   

## API

The API is composed of only two endpoints.

### Endpoints

#### GET /data/count?uid=<String>&date=<ISOString>

This endpoint has two required query parameters `uid` and `date`.
It returns the number of `data` elements in mongo that have `uid` and were
added on the same day as `date`.

**Example Response**
```
{
	"count": 4
}
```

#### POST /data/batch

This endpoint takes a json in the body of the request.

**Example Request**
```
[
	{
	    "uid": "1",
	    "name": "John Doe",
	    "date": "2015-05-12T14:36:00.451765",
	    "md5checksum": "e8c83e232b64ce94fdd0e4539ad0d44f"
	}
]
```

The request can have a variable amount of objects in the body array. Each of the objects must have all of the fields above. The `md5checksum` must be equal to the md5 hash of the other three values.

So in the example above, the `md5checksum` e8c83e232b64ce94fdd0e4539ad0d44f
must equal `md5('{"date": "2015-05-12T14:36:00.451765", "uid": "1", "name": "John Doe"}')`

The request is only successful if **all** of the objects in the requests 
are valid and the `md5checksum` is correct.

A successful response is an empty body with the status code `201`.

### Errors

The API will respond with errors on the following format.
```
{
	code: 1003,
	message: "A uid and a date are required"
}
```

