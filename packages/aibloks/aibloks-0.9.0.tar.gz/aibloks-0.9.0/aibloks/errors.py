class AiBloksException(Exception):

    def __init__(self, response):
        self.response = response
        try:
            self.status_code = response.status_code
            self.reason = response.json()["message"]
        except AttributeError:
            self.status_code = "-1"
            self.reason = response

        super().__init__(
            f"{self.status_code} {self.reason}"
        )