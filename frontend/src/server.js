var express = require('express'),
    ejs = require('ejs'),
    q = require('q'),
    bodyParser = require('body-parser'),
    beerLogbook = require('./client/beer-logbook'),
    breweryDB = require('./client/brewery-db');

var app = express();
app.set('view engine', 'ejs');
app.use(express.static(__dirname + '/public'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

app.get('/', function(req, res) {
    res.redirect('/search');
});

app.get('/search', function(req, res) {
    // the name query string is _always_ needed for BreweryDB
    if (req.query.name === undefined || req.query.name === '') {
        req.query.name = '*';
    };
    breweryDB.get('/beers', req.query).then(
        function(data) {
            res.render('search.ejs', {data: data});
        },
        function(error) {
            // TODO - add better error handling
            res.render('error.ejs');
        }

    ).done()
});

app.post('/search', function(req, res) {
    var options = {
        'comment': req.body.comment,
        'rating': req.body.rating,
        'brewerydb_id': req.body.brewerydb_id || ''
    };
    beerLogbook.put('/beer/' + req.body.name, options).then(
        function(data) {
            res.redirect('/search');
        },
        function(error) {
            // TODO - add error handling
            res.redirect('/search');
        }
    ).done()

    // the name query string is _always_ needed for BreweryDB
    if (req.query.name === undefined || req.query.name === '') {
        req.query.name = '*';
    };
    breweryDB.get('/beers', req.query).then(
        function(data) {
            res.render('search.ejs', {data: data});
        },
        function(error) {
            // TODO - add better error handling
            res.render('error.ejs');
        }

    ).done()
});

app.get('/my-beers', function(req, res) {
    var userData = {},
        promises = [];

    beerLogbook.get('/beers').then(
        function(data) {
            // Keep track of my rating and comments
            userData = data;
            // Retrieve rest of info for my beers from BreweryDB
            Object.keys(data).forEach(function(beer) {
                promises.push(
                    breweryDB.get('/beer/' + data[beer].brewerydb_id, {})
                );
            });
            return promises;
        }
    ).spread(
        function (results) {
            var breweryDBData = Array.prototype.slice.call(arguments);
            res.render(
                'my-beers.ejs', {data: breweryDBData, userData: userData}
            );
        }
    ).fail(
        function(error) {
            // TODO - add better error handling
            res.render('error.ejs');
        }
    ).done()
});

app.listen(5001);
console.log('Listening on ' + 5001);
