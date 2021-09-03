from wagtail.embeds.finders.base import EmbedFinder


class OSMFinder(EmbedFinder):
    """OpenStreetMap.org embed"""

    def __init__(self, **options):
        pass

    def accept(self, url):
        """
        Returns True if this finder knows how to fetch an embed for the URL.
        This should not have any side effects (no requests to external servers)
        """

        if not url.startswith("https://www.openstreetmap.org/export/embed.html"):
            return False
        return True

    def find_embed(self, url, max_width=None):
        """
        Takes a URL and max width and returns a dictionary of information about the
        content to be used for embedding it on the site.

        This is the part that may make requests to external APIs.
        """

        return {
            # 'title': "",
            "author_name": "OpenStreetMap contributors",
            "provider_name": "OpenStreetMap.org",
            "type": "rich",
            # 'thumbnail_url': "URL to thumbnail image",
            "width": 425,
            "height": 350,
            "html": f"""<div class='osm-embed'><iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="{url}" style="border: 1px solid black"></iframe><br/><small><a href="https://www.openstreetmap.org/#map=14/54.7747/-1.5886">View Larger Map</a></small></div>""",
        }
