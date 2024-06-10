import uuid
import pathlib
from django.utils.text import slugify


def train_image_path(instance, filename):
    filename = (
        f"{slugify(instance.name)}_{uuid.uuid4()}" + pathlib.Path(filename).suffix
    )
    return pathlib.Path("uploads/trains/") / pathlib.Path(filename)
