class InvalidEndpointException(Exception):
    def __init__(self, endpoint: str):
        super().__init__(f"Invalid endpoint: {endpoint}")
