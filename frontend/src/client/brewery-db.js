var q = require('q'),
    request = require('request');

var backend_url = 'http://api.brewerydb.com/v2',
    apiKey = 'cba371eb9abbb1952dc1b82bb30003ee';

exports.get = function(endpoint, options) {
    var d = q.defer(),
        queryParameters = ['key=' + apiKey];

    Object.keys(options).forEach(function(key) {
        queryParameters.push(String(key) + '=' + String(options[key]));
    });

    request({
            'url': backend_url + endpoint + '?' + queryParameters.join('&'),
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
