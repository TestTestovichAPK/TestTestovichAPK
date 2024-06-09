import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import pyaudio
import numpy as np

kivy.require('2.3.0')

class SoundAnalyzer(BoxLayout):
    def __init__(self, **kwargs):
        super(SoundAnalyzer, self).__init__(**kwargs)
        self.label = Label(text="Frequency: N/A")
        self.add_widget(self.label)

        self.sample_rate = 44100
        self.chunk = 1024

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.sample_rate,
                                  input=True,
                                  frames_per_buffer=self.chunk)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def update(self, dt):
        data = np.frombuffer(self.stream.read(self.chunk, exception_on_overflow=False), dtype=np.int16)
        fft = np.fft.fft(data)
        frequencies = np.fft.fftfreq(len(fft))
        idx = np.argmax(np.abs(fft))
        freq = abs(frequencies[idx] * self.sample_rate)
        self.label.text = f"Frequency: {freq:.2f} Hz"

    def on_stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

class SoundAnalyzerApp(App):
    def build(self):
        return SoundAnalyzer()

    def on_stop(self):
        self.root.on_stop()

if __name__ == '__main__':
    SoundAnalyzerApp().run()
