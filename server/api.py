from flask import Flask
from flask_restful import Resource, Api, reqparse
from preprocessing import Preprocessing
import json
from requests import request
import os
from flask_socketio import SocketIO, send

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'

socketIo = SocketIO(app, cors_allowed_origins="*")

app.debug = True

@socketIo.on('connect')
def connected():
    with open('temp.json') as readTemp:
        tempJson = json.load(readTemp)
    with open('temp.json', 'w') as output:
        tempJson['sekolah'] = ''
        tempJson['start'] = False
        json.dump(tempJson, output)

@socketIo.on("message")
def handleMessage(msg):
    answer = post(msg)
    message = answer['response']
    if (answer['type'] == 'with-data'):
        for eachData in answer['data']:
            message += "\n-{} ({})".format(eachData['nama_sekolah'], eachData['status'])
    send(message, broadcast=True)
    return None

def post(teks):
    text_process = Preprocessing()
    tokens = text_process.execute(teks)
    i = 0
    findKecamatan = False
    token_kecamatan = []
    target = ""
    response = -1
    tempJson = -1
    with open('temp.json') as readTemp:
        tempJson = json.load(readTemp)
    if (tokens[0] == 'reset'):
        with open('temp.json', 'w') as output:
            tempJson['sekolah'] = ''
            tempJson['start'] = False
            json.dump(tempJson, output)
        response = {
            "response": "Hai dik, silahkan sapa kami dengan hai/halo, untuk memulai BOT. Atau kalau mau ajak kenalan dengan mengetik 'kenalan dong' buat kepo soal BOT ini juga bisa! :)",
            "type": "no-data"
        }
    if (tempJson['start'] == False):
        if (tokens[0] == 'hai' or tokens[0] == 'halo'):
            tempJson['start'] = True
            with open('temp.json', 'w') as writeTemp:
                json.dump(tempJson, writeTemp)
            return {
                "response": "Hai dik, ada yang bisa BOT bantu?",
                "type": "no-data"
            }
        elif tokens[0] == 'kenal':
            return  {
                "response": "BOT ini adalah BOT yang akan membantu adik-adik untuk mencari sekolah di Kota Bandung, berdasarkan kecamatan yang ingin adik-adik cari. BOT ini memanfaatkan API dari http://data.bandung.go.id/",
                "type": "no-data"
            }
        return  {
            "response": "Hai dik, silahkan sapa kami dengan hai/halo, untuk memulai BOT. Atau kalau mau ajak kenalan dengan mengetik 'kenalan dong' buat kepo soal BOT ini juga bisa! :)",
            "type": "no-data"
        }
    for eachToken in tokens:
        if (tempJson['sekolah'] != ''):
            with open('temp.json') as readTemp:
                tempJson = json.load(readTemp)
            if (eachToken != 'camat'):
                token_kecamatan.append(eachToken)
                text_kecamatan = "-".join(token_kecamatan)
                with open('manifest.json') as file_sekolah:
                    data_sekolah = json.load(file_sekolah)
                    for eachData in data_sekolah['sekolah']:
                        if (eachData['kecamatan'] == text_kecamatan):
                            dataFetch = request('GET', eachData[tempJson['sekolah']]).json()
                            response = {
                                "response": "Hei dik, berikut daftar sekolah yang dicari! Ada yang bisa BOT bantu lagi? Ketik 'selesai' jika ingin mengakhiri percakapan :)",
                                "data": dataFetch['data'],
                                "type": "with-data"
                            }
                            with open('temp.json', 'w') as output:
                                tempJson['sekolah'] = ''
                                tempJson['start'] = True
                                json.dump(tempJson, output)
            if (eachToken == 'selesai'):
                with open('temp.json', 'w') as output:
                    tempJson['sekolah'] = ''
                    tempJson['start'] = False
                    json.dump(tempJson, output)
                response = {
                    "response": "Baik, terimakasih sudah menggunakan BOT ini! :)",
                    "type": "no-data"
                }
                break
        else:
            if (eachToken == 'sekolah'):
                response = {
                    "response": "Hai dik, mau cari sekolah jenjang mana?",
                    "type": "no-data"
                }
                break
            if (eachToken == 'sd'):
                with open('temp.json', 'w') as output:
                    tempJson['sekolah'] = 'sd'
                    findKecamatan = True
                    json.dump(tempJson, output)
                response = {
                    "response": "Hai dik, mau cari SD di kecamatan mana?",
                    "type": "no-data"
                }
                break
            if (eachToken == 'smp'):
                with open('temp.json', 'w') as output:
                    tempJson['sekolah'] = 'smp'
                    findKecamatan = True
                    json.dump(tempJson, output)
                response = {
                    "response": "Hai dik, mau cari SMP di kecamatan mana?",
                    "type": "no-data"
                }
                break
            if (eachToken == 'sma'):
                with open('temp.json', 'w') as output:
                    tempJson['sekolah'] = 'sma'
                    findKecamatan = True
                    json.dump(tempJson, output)
                response = {
                    "response": "Hai dik, mau cari SMA di kecamatan mana?",
                    "type": "no-data"
                }
                break
            if (eachToken == 'selesai'):
                with open('temp.json', 'w') as output:
                    tempJson['sekolah'] = ''
                    tempJson['start'] = False
                    json.dump(tempJson, output)
                response = {
                    "response": "Baik, terimakasih sudah menggunakan BOT ini! :)",
                    "type": "no-data"
                }
                break
    if (response == -1):
        return {
            "response": "Maaf dik, BOT tidak paham yang adik tanyakan :(",
            "type": "no-data"
        }
    else:
        return response

if __name__ == "__main__":
    if os.path.isfile('temp.json') == False:
        with open('temp.json', 'w') as output:
            json.dump({"sekolah": "", "start": False}, output)
    socketIo.run(app, host='0.0.0.0', port=5000)