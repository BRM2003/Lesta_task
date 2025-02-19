from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


def validate_file_extension(value):
    if value.file.content_type != 'text/plain':
        raise ValidationError(u'File format should be .txt')


class File(models.Model):
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, name='user_file', null=True, blank=True)
    file_name = models.CharField(max_length=50)
    format = models.CharField(max_length=10)
    path = models.FileField(upload_to="%Y/%m/%d/", validators=[validate_file_extension])
    active = models.BooleanField(default=True)
    cr_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    up_on = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["file_name"], name="file_index_by_name"),
            models.Index(fields=["active", "file_name"], name="active_file_index_by_name"),
            models.Index(fields=["format", "file_name"], name="file_index_by_format_and_name")
        ]
        verbose_name_plural = 'Files'
        verbose_name = 'File'

    def __str__(self):
        return f"{self.id} - {self.file_name}"


class Word(models.Model):
    word_value = models.CharField(max_length=50, unique=True)
    active = models.BooleanField(default=True)
    cr_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    up_on = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["word_value", "active"], name="active_word_index"),
        ]
        verbose_name_plural = 'Words'
        verbose_name = 'Word'

    def __str__(self):
        return self.word_value


class WordsInFiles(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(validators=[MinValueValidator(1, message='Must be at least 1 word in file')])
    active = models.BooleanField(default=True)
    cr_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    up_on = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["file", "word"], name="connect_indx_by_word_and_file"),
        ]
        verbose_name_plural = 'Words in Files'
        verbose_name = 'Word in File'

    def __str__(self):
        return f"{self.file} - {self.word}"
