import json
import requests
import wave

class talk():
    @staticmethod
    def generate_wav(text, speaker=1, filepath='./audio.wav'):
        host = 'localhost'
        port = 50021

        # audio_query
        response1 = requests.post(
            f'http://{host}:{port}/audio_query',
            params={'text': text, 'speaker': speaker}
        )
        if response1.status_code != 200:
            raise RuntimeError('audio_query failed')

        # synthesis
        headers = {'Content-Type': 'application/json'}
        response2 = requests.post(
            f'http://{host}:{port}/synthesis?speaker={speaker}',
            headers=headers,
            data=json.dumps(response1.json())
        )
        if response2.status_code != 200:
            raise RuntimeError('synthesis failed')

        # save as wav
        with wave.open(filepath, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)
            wf.writeframes(response2.content)

if __name__ == '__main__':
    talk.generate_wav('こんにちは！')
