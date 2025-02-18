from django.shortcuts import render


def file_loader(request):
    response = {}
    try:
        if request.method == 'POST':
            if request.POST['file'][-4:] != '.txt':
                raise Exception('Формат файла должен быть .txt')
    except Exception as e:
        response['success'] = False
        response['message'] = str(e)
    return render(request, 'file_upload_form.html', response)