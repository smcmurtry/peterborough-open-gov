var fs = require('fs');
const Fuse = require('fuse.js')

var data = JSON.parse(fs.readFileSync('./scraping/search_data.json', 'utf8'));
// console.log(data)

const options = {
  includeScore: true,
  // Search in `author` and in `tags` array
  keys: ['body']
}

const fuse = new Fuse(data, options)

const result = fuse.search('omicron');
