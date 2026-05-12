import simpleaudio as sa

def pop_hint():
    wave_obj = sa.WaveObject.from_wave_file("pop.wav")
    play_obj = wave_obj.play()  # non-blocking
    play_obj.wait_done()        # <- wait until finished
