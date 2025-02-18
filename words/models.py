from django.conf import settings
from django.db import models


class File(models.Model):
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, name='user_file')
    file_name = models.CharField(max_length=50, null=False, blank=False)
    format = models.CharField(max_length=10, null=False, blank=False)
    path = models.FileField(upload_to="%Y/%m/%d/")
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
    word_value = models.CharField(max_length=50, unique=True, null=False, blank=False)
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
    file = models.ForeignKey(File, on_delete=models.CASCADE, name='file_connection', blank=True, null=True)
    word = models.ForeignKey(Word, on_delete=models.CASCADE, name='word_connection', blank=True, null=True)
    count = models.PositiveIntegerField(null=False, blank=False)
    active = models.BooleanField(default=True)
    cr_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    up_on = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["file_connection", "word_connection"], name="connect_indx_by_word_and_file"),
        ]
        verbose_name_plural = 'Words in Files'
        verbose_name = 'Word in File'

    def __str__(self):
        return f"{self.file} - {self.word}"
