import re
from datetime import datetime

from ..dataformats import Event

link_extract_regex = r"(https?://.+?)([ ,\n\\<>]|$)"
geoconfirmed_regex = r"https://twitter\.com/GeoConfirmed/status/(\d+)([ ,\n]|$)"  # noqa

class GeoConfirmedProcessor():
    @staticmethod
    def extract_events(data, eventtype=None):

        events = []

        def is_relevant(folder):
            # Filter out metadata folders
            if folder.get('name')[:2] in ('A.', 'B.'):
                return False
            return True

        folders = filter(
            is_relevant,
            data.get('mapDataFolders')
        )

        # Example: "2022-10-10T16:20:00"
        DATE_INPUT_FORMAT = "%Y-%m-%dT%H:%M%S"

        def parse_date(d):
            # Note: e.g. twitter.com/GeoConfirmed/status/1579567301963440128
            # has a wrong date (twitter id instead of date string)
            try:
                return datetime.strptime(d, DATE_INPUT_FORMAT)
            except ValueError:
                return None

        for folder in folders:
            placemarks = folder.get('mapDataPlacemarks')
            if not placemarks:
                continue

            for item in placemarks:
                sources = []
                if (links := re.findall(link_extract_regex,
                                        item.get('description'))):
                    sources.extend((link for link, _unused in links))

                def get_id(desc):
                    status = re.findall(geoconfirmed_regex, desc)
                    if status:
                        return status[0][0]
                    return None

                event = Event(
                    id=get_id(item.get('description')),
                    date=parse_date(item.get('date') or ''),
                    # Coordinates swapped
                    latitude=float(item.get('coordinates')[1]),
                    longitude=float(item.get('coordinates')[0]),
                    place_desc=None,
                    title=item.get('name'),
                    description=item.get('description'),
                    sources=sources,
                )
                events.append(event)

        return events
