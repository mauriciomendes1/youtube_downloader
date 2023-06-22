#baixador de vídeos do youtube com pysimplegui
import PySimpleGUI as sg
from pytube import YouTube
import os

sg.theme('GreenMono')

def principal():
    global window
    layout = [
        [sg.Text('URL', size=(4,1)), sg.InputText('', size=(33,1), key='-URL-')],
        [sg.Radio('MP4', '-TYPE-', key='-MP4-'), sg.Radio('MP3', '-TYPE-', key='-MP3-')],
        [sg.Text('Local to save:'), sg.FolderBrowse(key='-PATH-')],
        [sg.Text('', key='-CONC-', size=(30, 1))],
        [sg.Button('Download', key='-DOWN-'), sg.Progress(100, size=(20,15), key='-PROGRESS-')]
        
    ]

    window = sg.Window('Youtube vídeo download', layout, size=(300, 160))

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == '-DOWN-' and values['-MP4-']:
            if values['-URL-'] != '' and values['-PATH-'] != '':
                download(values['-URL-'], values['-PATH-'], 'mp4')
            else:
                pass
        if event == '-DOWN-' and values['-MP3-']:
            if values['-URL-'] != '' and values['-PATH-'] != '':
                download(values['-URL-'], values['-PATH-'], 'mp3')
            else:
                pass


def download(url, path, type):
    
    try:
        yt = YouTube(url, on_progress_callback=progress_bar)
    except:
        return 'Connection error!'

    if type == 'mp4':
        video = yt.streams.filter(progressive=True, file_extension='mp4').first()
        video.download(path)

    #download somente do aúdio
    elif type == 'mp3':
        #extraindo o áudio
        video = yt.streams.filter(only_audio=True).first()
        #baixando o áudio
        audio = video.download(path)

        #salvando o áudio
        base, ext = os.path.splitext(audio)
        new_file = base + '.mp3'
        os.rename(audio, new_file)


def progress_bar(stream, chunk, bytes_remaning):
    window['-PROGRESS-'].update(100 - round(bytes_remaning / stream.filesize * 100))
    if bytes_remaning == 0:
        window['-CONC-'].update('Download concluido!')
principal()