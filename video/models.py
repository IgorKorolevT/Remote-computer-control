from django.db import models
from functools import partial
from pathlib import Path
from django.utils import timezone
from django.utils.text import slugify


def get_file_name(instance, file_name: str, folder_name: Path):
    old_file_name = Path(file_name)
    new_file_name = slugify(old_file_name.stem) + timezone.now().strftime("%Y%m%d%H%M%S%f") + old_file_name.suffix
    return folder_name / new_file_name


# Create your models here.
class Video(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default="No provided")
    url = models.URLField()
    preview = models.ImageField(upload_to=partial(get_file_name, folder_name=Path("video_preview")), null=True,
                                blank=True)
