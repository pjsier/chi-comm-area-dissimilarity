# Chicago Community Areas - Index of Dissimilarity

Inspired by Curious City and City Bureau's [article about segregation in Chicago](https://www.wbez.org/shows/curious-city/is-notoriously-segregated-chicago-becoming-integrated/5dc5045b-6b0d-41c9-81b7-ecc52b76a222)
looking at the [index of dissimilarity measure of segregation](https://en.m.wikipedia.org/wiki/Index_of_dissimilarity)
for individual community areas, rather than the city as a whole.

## Setup

You'll need GNU Make and `ogr2ogr` installed. If you have each of those, clone
this directory, copy the `key.mk.sample` file into `key.mk` with your own credentials
(if you don't have a key, you can get one [on the Census site](https://www.census.gov/developers/)),
and run `make all` to add all data to the `data/` directory.
