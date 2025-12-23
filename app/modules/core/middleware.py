class IframeReferrerMiddleware:
    YOUTUBE_MARKERS = (
        "youtube.com",
        "youtu.be",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if "text/html" not in response.get("Content-Type", ""):
            return response

        content = response.content.decode("utf-8").lower()
        iframes = content.split("<iframe")
        has_youtube_iframe = False

        for iframe in iframes[1:]:
            iframe_tag = iframe.split(">", 1)[0] + ">"
            if any(marker in iframe_tag for marker in self.YOUTUBE_MARKERS):
                has_youtube_iframe = True
                break 

        if has_youtube_iframe:
            response["Referrer-Policy"] = "no-referrer"

        return response
