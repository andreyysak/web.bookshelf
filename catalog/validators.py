from pathlib import Path

from django.core.exceptions import ValidationError

MAX_COVER_SIZE = 2 * 1024 * 1024
ALLOWED_COVER_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def validate_cover(file):
    if file.size > MAX_COVER_SIZE:
        raise ValidationError("Cover must be 2 MB or smaller.")
    if Path(file.name).suffix.lower() not in ALLOWED_COVER_EXTENSIONS:
        raise ValidationError("Only jpg, png and webp images are allowed.")
