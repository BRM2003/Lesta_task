from django.shortcuts import render
from collections import Counter
from .models import *
from .forms import FILE_NAME, FileUploadForm
import re


def file_loader(request):
    response = {}
    try:
        if request.method == 'POST':
            form = FileUploadForm(request.POST, request.FILES)
            uploaded_file = request.FILES.get(FILE_NAME)

            if not uploaded_file.name.endswith('.txt'):
                raise Exception('Формат файла должен быть .txt')

            if not form.is_valid():
                raise Exception('Не корректный формат файла')

            file = save_file(form, uploaded_file, request.user)

            with open(file.path.path, "r", encoding="utf-8") as f:
                text = f.read()
                words = re.findall(r'\b\w+\b', text.lower())
                word_count, word_list = count_of_words(words)

            save_new_words(word_list)
            save_words_in_files(file, word_count)

            response['form'] = form
        else:
            response['form'] = FileUploadForm()
    except Exception as e:
        response['success'] = False
        response['message'] = str(e)
    return render(request, 'file_upload_form.html', response)


def save_file(form, file, user=None):
    obj = form.save(commit=False)
    obj.path = file
    obj.users = user
    obj.file_name = file.name
    obj.format = str(file.name).split('.')[-1]
    obj.save()
    return obj


def count_of_words(word_list):
    words = Counter(word_list)
    return dict(words), list(words)


def save_new_words(words_list):
    existing_words = set(Word.objects.values_list('word_value', flat=True))
    new_words = [Word(word_value=word) for word in words_list if word not in existing_words]

    if new_words:
        Word.objects.bulk_create(new_words)


def save_words_in_files(file, word_counts):
    existing_words = {word.word_value: word.id for word in Word.objects.filter(word_value__in=word_counts.keys())}
    word_file_entries = [
        WordsInFiles(
            file=file,
            word_id=existing_words[word],
            count=count
        )
        for word, count in word_counts.items() if word in existing_words
    ]

    if word_file_entries:
        WordsInFiles.objects.bulk_create(word_file_entries)

