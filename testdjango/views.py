'''
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import default_storage

def Range(a, b):
    ret = []
    for i in range(a, b):
        ret.append(i)
    return ret

def index(request):
    return render(request, 'index.html')

def nxt(request):
    file = request.FILES["fu"]
    file_name = default_storage.save('media/' + file.name, file)

    return render(request, 'next.html', {"file_name": file.name})

def func(request, question_id):
    return render(request, 'num.html', { "num": question_id, "range": Range(1, 11)})

def fff(request, method):
    ret = ""
    if method == 'youtube':
        ret += "선택한 방법: {}<br>입력한 URL: {}".format("Youtube", request.POST["info"])
    else:
        ret += "선택한 방법: {}<br>업로드한 파일 이름: {}".format("Local File", request.FILES["info"].name)

    return HttpResponse(ret)

def ff2(request, method):
    if method == 'youtube':   
        return render(request, 'Utube.html') 
    else:   
        return render(request, 'local.html') '''

from django.shortcuts import render, redirect

# Create your views here.
from .forms import *
from .models import *

def board(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        writer = request.POST['writer']

        board = Board(
            title=title,
            content=content,
            writer=writer,
        )
        board.save()
        return redirect('board')
    else:
        boardForm = BoardForm
        board = Board.objects.all()
        context = {
            'boardForm': boardForm,
            'board': board,
        }

        return render(request, 'board.html', {"context": context, "board": board})

def edit(request, id):
    board = Board.objects.get(id=id)
    if request.method == 'POST':
        board.title = request.POST['title']
        board.content = request.POST['content']
        board.writer = request.POST['writer']

        board.save()
        return redirect('board')
    else:
        boardForm = BoardForm
        return render(request, 'update.html', {"boardForm": BoardForm})

def delete(request, id):
    board = Board.objects.get(id=id)
    board.delete()
    return redirect('board') 

def func():
    from google.cloud import speech_v1p1beta1 as speech

    client = speech.SpeechClient()

    speech_file = "resources/commercial_mono.wav"

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code="en-US",
        enable_speaker_diarization=True,
        diarization_speaker_count=2,
    )

    print("Waiting for operation to complete...")
    response = client.recognize(config=config, audio=audio)

    # The transcript within each result is separate and sequential per result.
    # However, the words list within an alternative includes all the words
    # from all the results thus far. Thus, to get all the words with speaker
    # tags, you only have to take the words list from the last result:
    result = response.results[-1]

    words_info = result.alternatives[0].words

    # Printing out the output:
    for word_info in words_info:
        print(
            u"word: '{}', speaker_tag: {}".format(word_info.word, word_info.speaker_tag)
        )

func()