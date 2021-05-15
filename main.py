import io
import os
import time
from collections import Counter
from tempfile import NamedTemporaryFile

import cv2
import numpy as np
import pyautogui
from gtts import gTTS
from mpg123 import Mpg123, Out123


def get_screen_image():
    with NamedTemporaryFile() as f:
        pil_image = pyautogui.screenshot(imageFilename=f.name)

    opencvImage = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    return opencvImage


def extract_qr_codes(image):
    qrCodeDetector = cv2.QRCodeDetector()
    res = qrCodeDetector.detectAndDecodeMulti(image)
    return Counter(res[1])


def audio_describe(codes):
    text = ''
    for code, count in codes.items():
        if code == 'thumbs_up':
            text += f'{count} users are presenting thumbs-up, '
        elif code == 'smiling':
            text += f'{count} users are smiling, '

    if text == '':
        return

    with io.BytesIO() as f:
        gTTS(text=text, lang='en', slow=False).write_to_fp(f)
        f.seek(0)
        mp3 = Mpg123()
        mp3.feed(f.read())
        out = Out123()
        for frame in mp3.iter_frames(out.start):
            out.play(frame)


if __name__ == '__main__':
    while True:
        # Sanity check using a pre-made image.
        # Comment out the get_screen_image() call to test this.
        # image = cv2.imread('multi.png')

        s = time.perf_counter()
        image = get_screen_image()
        print(f'Screenshot time: {time.perf_counter() - s:0.2f} secs')

        s = time.perf_counter()
        codes_and_counts = extract_qr_codes(image)
        print(f'QR extraction time: {time.perf_counter() - s:0.2f} secs')
        if len(codes_and_counts) > 0:
            s = time.perf_counter()
            audio_describe(codes_and_counts)
            print(f'Audio time: {time.perf_counter() - s:0.2f} secs')
        else:
            print('No QR codes detected')
