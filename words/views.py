import math
import re

from django.db.models import Count
from django.shortcuts import render
from collections import Counter
from .models import *
from .forms import FILE_NAME, FileUploadForm


def file_loader(request):
    response = {"page_title": 'LestaTask', 'success': True}
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

            results_tf = calculate_tf(word_count)
            results_idf = calculate_idf(word_count)

            response['result'] = summarize_tf_and_idf(results_tf, results_idf, word_count)
            response['success'] = True

            return render(request, "table.html", response)
        else:
            response['form'] = FileUploadForm()
    except Exception as e:
        print(str(e))
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


def calculate_tf(words_count):
    word_c = words_count.copy()
    total_words = sum(list(map(lambda item: word_c[item], word_c)))

    for word in word_c:
        word_c[word] = round(word_c[word] / total_words, 4)

    return word_c


def calculate_idf(word_list):
    total_documents = File.objects.count()

    words_with_doc_count = Word.objects.annotate(
        doc_count=Count("wordsinfiles__file", distinct=True)
    ).filter(word_value__in=word_list).values("word_value", "doc_count")

    idf_values = {
        word["word_value"]: round(math.log(total_documents / word["doc_count"], 10), 4)
        for word in words_with_doc_count
    }

    return idf_values


def summarize_tf_and_idf(tf, idf, word_count):
    result = []
    for word in word_count:
        result.append(
            {
                "word": word,
                "count": word_count[word],
                "tf": tf[word],
                "idf": idf[word],
                "word_weight": round(tf[word] * idf[word], 4)
            }
        )

    result = sorted(result, key=lambda item: item['idf'], reverse=True)
    return result[:50]

