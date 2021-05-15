import io
import os
from collections import Counter

import cv2
import numpy as np
from gtts import gTTS
from mpg123 import Mpg123, Out123


def extract_qr_codes():
    image = cv2.imread('multi.png')
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

    with io.BytesIO() as f:
        gTTS(text=text, lang='en', slow=False).write_to_fp(f)
        f.seek(0)
        mp3 = Mpg123()
        mp3.feed(f.read())
        out = Out123()
        for frame in mp3.iter_frames(out.start):
            out.play(frame)


if __name__ == '__main__':
    codes_and_counts = extract_qr_codes()
    audio_describe(codes_and_counts)
