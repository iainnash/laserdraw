var fs = require('fs');
var ndjson = require('ndjson'); // npm install ndjson
var express = require('express');
const app = express()
const port = 3030

const MAX_COUNT = 2000;

var drawings = [];
function parseSimplifiedDrawings(fileName, callback) {
  var fileStream = fs.createReadStream(fileName)
  fileStream
    .pipe(ndjson.parse())
    .on('data', function(obj) {
			if (drawings.length < MAX_COUNT) {
				drawings.push(obj)
			}
    })
    .on('error', callback)
    .on('end', function() {
      callback(null, drawings)
    });
}

parseSimplifiedDrawings("data/full_simplified_t-shirt.ndjson", function(err, drawings) {
  if(err) return console.error(err);
  drawings.forEach(function(d) {
    // Do something with the drawing
    console.log(d.key_id, d.countrycode);
  })
  console.log("# of drawings:", drawings.length);
})


app.get('/t-shirts', (req, res) => res.send({drawings}));
app.get('/drawing', (req, res) => res.send(drawings[0]))
app.use(express.static('public'));

app.listen(port, () => console.log('listening on http://localhost:3030/'));
