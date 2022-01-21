var express = require("express");
var app = express();
var fs = require('fs');
const Fuse = require('fuse.js')

var data = JSON.parse(fs.readFileSync('./scraping/search_data.json', 'utf8'));

const options = {
  includeScore: true,
  includeMatches: true,
//   threshold: 0.0,
  ignoreLocation: true,
  findAllMatches: true,
  useExtendedSearch: true,
//   minMatchCharLength: 4,
  // Search in `author` and in `tags` array
  keys: ['body']
}

const fuse = new Fuse(data, options)


app.listen(3000, () => {
 console.log("Server running on port 3000");
});

app.get("/search", (req, res, next) => {
    const text = req.query.text
    console.log(text)
    const result = fuse.search(`'${text}`);
    res.json(result.slice(0, 10));
});
