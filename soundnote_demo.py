import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import threading
import time

# ---------- 参数 ----------
duration = 2.0
frequency = 440
sample_rate = 44100
block_size = 1024
amplitude = 0.5

t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
signal = (amplitude * np.sin(2 * np.pi * frequency * t)).astype(np.float32)

# ---------- 播放线程 ----------
def play_stream():
    i = 0
    with sd.OutputStream(samplerate=sample_rate, channels=1, dtype='float32') as stream:
        while i < len(signal):
            chunk = signal[i:i+block_size]
            if len(chunk) == 0:
                break
            stream.write(chunk.reshape(-1, 1))
            i += block_size

# ---------- 绘图线程 ----------
def draw_waveform():
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 3))
    line, = ax.plot([], [], lw=2)
    ax.set_ylim(-1, 1)
    ax.set_xlim(0, block_size)
    ax.set_title("Real-Time Waveform on M1")
    ax.set_xlabel("Samples")
    ax.set_ylabel("Amplitude")

    for i in range(0, len(signal), block_size):
        chunk = signal[i:i+block_size]
        line.set_ydata(chunk)
        line.set_xdata(np.arange(len(chunk)))
        ax.set_xlim(0, len(chunk))
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(block_size / sample_rate * 0.9)

    plt.ioff()
    plt.show()

# ---------- 主程序 ----------
if __name__ == "__main__":
    t1 = threading.Thread(target=play_stream)
    t1.start()
    draw_waveform()
    t1.join()