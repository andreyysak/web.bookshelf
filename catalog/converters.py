class ISBNConverter:
    regex = r'(?:\d{10}|\d{13})'

    def to_python(self, value):
        return value

    def to_url(self, value):
        if not isinstance(value, str) or not value.isdigit() or len(value) not in (10, 13):
            raise ValueError('ISBN must contain 10 or 13 digits')

        return value