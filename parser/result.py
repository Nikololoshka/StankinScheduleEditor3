class ParserResult:
    def __init__(
            self,
            path: str,
            name: str,
            pairs=None,
            error=None
    ):
        self.name = name
        self.path = path
        self.pairs = [] if pairs is None else pairs
        self.error = error

    def has_error(self):
        return self.error is not None

    def __str__(self):
        return f'ParserResult(name={self.name}, pairs={len(self.pairs)})'
