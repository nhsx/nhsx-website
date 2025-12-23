class IframeReferrerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if "text/html" in response.get("Content-Type", ""):
            content = response.content.decode("utf-8")

            if "<iframe" in content.lower():
                response["Referrer-Policy"] = "no-referrer"

        return response
