# Usage example: Extracting geo points from Bellingcat database
# Returns valid GeoJSON

from geo_extractor.downloaders import BellingcatDownloader
from geo_extractor.processors import (
    BellingcatProcessor,
    format_as_geojson,
)

d = BellingcatDownloader()
data = d.download()

p = BellingcatProcessor()
events = p.extract_events(data)

events_geojson = format_as_geojson(events)
print(events_geojson)

# Alternatively, using @dataclass FeatureCollection:
# Requires changing the __repr__ func for the datetime obj
# import json
# from geo_extractor.processors import format_as_featurecollection
# events_geojson = format_as_featurecollection(events).__dict__
# print(json.dumps(events_geojson))
