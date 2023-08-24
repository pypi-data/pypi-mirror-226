import pyaudio
from pyaudio import PyAudio, paInt16
import numpy as np
import wave
import time
import os


class AudioRecorder(object):
    print("AudioRecorder")
    NUM_SAMPLES = 1280  # pyaudio内置缓冲大小
    SAMPLING_RATE = 16000  # 取样频率
    AUDIO_STRENGTH_THR = 500  # 有效声音的声音强度判定阈值
    VALID_SAMPLE_NUMTHR = 20  # 有效声音的总长度阈值
    # MIN_RECORD_LENGTH = 20  # 声音记录的最小长度：MIN_RECORD_LENGTH * NUM_SAMPLES 个取样
    DELAY_RECORD_LENGTH = 1  # 检测到有效声音延迟录音
    # MAX_RECORD_TIME = 100  # 录音时间

    voicestring = []

    def __init__(self, min_record_length=20, max_record_time=100):
        self.min_record_length = min_record_length
        self.max_record_time = max_record_time

    def savewav(self, filename):
        if os.path.exists(filename):
            os.remove(filename)
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(self.SAMPLING_RATE)
        wf.writeframes(np.array(self.voicestring).tostring())
        # wf.writeframes(self.Voice_String.decode())
        wf.close()

    def recoder(self, savepath=None):
        print("\n\nRecording start....")
        pa = PyAudio()
        stream = pa.open(format=paInt16,
                         channels=1,
                         rate=self.SAMPLING_RATE,
                         input=True,
                         frames_per_buffer=self.NUM_SAMPLES)
        audio_record_counter = self.min_record_length
        save_buffer = []
        maxtime_counter = self.max_record_time
        while True:
            maxtime_counter -= 1
            # 读入NUM_SAMPLES个取样, 将读入的数据转换为数组
            string_audio_data = stream.read(self.NUM_SAMPLES)
            audio_data = np.fromstring(string_audio_data, dtype=np.short)
            if maxtime_counter % 5 == 0:
                print("录音中....", audio_record_counter, maxtime_counter,
                      np.max(audio_data), len(audio_data))
            chunk = bytes(audio_data)

            # delay recorder if valid speech voice
            valid_sample_num = np.sum(audio_data > self.AUDIO_STRENGTH_THR)
            if valid_sample_num > self.VALID_SAMPLE_NUMTHR:
                audio_record_counter += self.DELAY_RECORD_LENGTH

            # 如果个数大于COUNT_NUM，则至少保存SAVE_LENGTH个块
            if audio_record_counter > 0:
                save_buffer.append(string_audio_data)
                audio_record_counter -= 1
            else:
                # 将save_buffer中的数据写入WAV文件，WAV文件的文件名是保存的时刻
                if len(save_buffer) > 0:
                    self.voicestring = save_buffer
                    save_buffer = []
                    print("Recode a piece of  voice successfully!")
                break
            if maxtime_counter == 0:
                if len(save_buffer) > 0:
                    self.voicestring = save_buffer
                    save_buffer = []
                    print("Recode a piece of  voice successfully!")
                break

        stream.stop_stream()
        stream.close()
        pa.terminate()

        if savepath is not None:
            self.savewav(savepath)
        print("Recording finished!\n\n")


def runner_audio_player_thread(thidx, wavdata_short):
    """
        play audio using stream data and send start-time to unity
    """
    print("Loop {} start!".format(thidx))
    player = pyaudio.PyAudio()
    stream = player.open(format=player.get_format_from_width(width=2),
                         channels=1,
                         rate=16000,
                         output=True)

    audioplay_st = time.time()
    # time.sleep(0.4)

    stream.write(wavdata_short.tobytes())
    print("Loop {} play finished, play time: {}!".format(
        thidx,
        time.time() - audioplay_st))
    stream.stop_stream()
    stream.close()
    player.terminate()
