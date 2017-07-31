include key.mk

GEO_BASE = https://www2.census.gov/geo/tiger/TIGER
DATA_API_BASE = https://api.census.gov/data

STATE = 17
COUNTY = 031

STD_COLS = state county tract block_group
2015_COLNAMES = geoid total white black amind asian pi not_hl_white hl $(STD_COLS)
2015_COLS = $(subst $(space),$(comma),$(strip $(2015_COLNAMES)))
2015_VARS = GEOID \
	B02001_001E \
	B02001_002E \
	B02001_003E \
	B02001_004E \
	B02001_005E \
	B02001_006E \
	B03002_003E \
	B03002_012E

2010_COLNAMES = total white black amind asian pi hl not_hl_white $(STD_COLS)
2010_COLS = $(subst $(space),$(comma),$(strip $(2010_COLNAMES)))
2010_VARS = P0080001 \
	P0080003 \
	P0080004 \
	P0080005 \
	P0080006 \
	P0080007 \
	P0090002 \
	P0090005

2000_COLNAMES = total white black amind asian hl not_hl_white $(STD_COLS)
2000_COLS = $(subst $(space),$(comma),$(strip $(2000_COLNAMES)))
2000_VARS = P003001 \
	P003003 \
	P003004 \
	P003005 \
	P003006 \
	P004002 \
	P004005

# Pulled from https://github.com/fitnr/get-tiger
TOCSV = 's/,null,/,,/g; \
	s/[["_]//g; \
	s/\]//g; \
	s/,$$//g; \
	s/^[0-9]*US//'

# For comma-delimited list
null :=
space := $(null) $(null)
comma := ,

2015_DATA_API = $(DATA_API_BASE)/2015/acs5?get=$(subst $(space),$(comma),$(strip $(2015_VARS)))&for=block+group:*&in=state:$(STATE)+county:$(COUNTY)&key=$(CENSUS_KEY)
2010_DATA_API = $(DATA_API_BASE)/2010/sf1?get=$(subst $(space),$(comma),$(strip $(2010_VARS)))&for=block+group:*&in=state:$(STATE)+county:$(COUNTY)&key=$(CENSUS_KEY)
2000_DATA_API = $(DATA_API_BASE)/2000/sf1?get=$(subst $(space),$(comma),$(strip $(2000_VARS)))&for=block+group:*&in=state:$(STATE)+county:$(COUNTY)&key=$(CENSUS_KEY)

.PHONY: clean

all: race geo

race: data/2015/census_race.csv data/2010/census_race.csv data/2000/census_race.csv

geo: data/2015/block_groups.geojson data/2010/block_groups.geojson data/2000/block_groups.geojson

data/%/census_race.csv:
	mkdir -p data/$*
	curl -s --get "$($*_DATA_API)" | sed $(TOCSV) > $@
	sed -i '' "1 s/.*/$($*_COLS)/" $@

data/%/block_groups.geojson:
	mkdir -p data/$*
	curl -s $(GEO_BASE)$*/BG/tl_$*_$(STATE)_bg.zip -o data/$*/tl_$*_$(STATE)_bg.zip
	unzip data/$*/tl_$*_$(STATE)_bg.zip -d data/$*
	ogr2ogr -f GeoJSON -t_srs crs:84 data/$*/block_groups.geojson data/$*/tl_$*_$(STATE)_bg.shp
	rm data/$*/tl_*

clean:
	rm -r data/2000 data/2010 data/2015
