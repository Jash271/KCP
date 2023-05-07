const {BloomFilter} = require('bloom-filters')
// create a Bloom Filter with a size of 10 and 4 hash functions
let filter = new BloomFilter(10000,10)

console.log(filter)
// insert data
filter.add('alice')
filter.add('bob')

const exported = filter.saveAsJSON()

let new_filter = BloomFilter.fromJSON(exported)

new_filter.add('Jash')
console.log(new_filter.has('archana')) 