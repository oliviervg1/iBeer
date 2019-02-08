var q = require('q'),
    request = require('request');

var backend_url = 'http://localhost:8080';

exports.get = function(endpoint) {
    var d = q.defer();
    request({
            'url': backend_url + endpoint,
            'json': true,
            'timeout': '10000'
        },
        function (error, response, body) {
            if (error || response.statusCode != 200) {
                d.reject(new Error(error));
            } else {
                d.resolve(body);
            }
        }
    );
    return d.promise;
}

exports.put = function(endpoint, data) {
    var d = q.defer();
    request({
            'method': 'PUT',
            'url': backend_url + endpoint,
            'body': data,
            'json': true,
            'timeout': '10000'
        },
        function (error, response, body) {
            if (error || response.statusCode != 201) {
                d.reject(new Error(error));
            } else {
                d.resolve(body);
            }
        }
    );
    return d.promise;
}

exports.delete = function(endpoint, data) {
    var d = q.defer();
    request({
            'method': 'DELETE',
            'url': backend_url + endpoint,
            'body': data,
            'json': true,
            'timeout': '10000'
        },
        function (error, response, body) {
            if (error || response.statusCode != 201) {
                d.reject(new Error(error));
            } else {
                d.resolve(body);
            }
        }
    );
    return d.promise;
}
