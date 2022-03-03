import simpleaudio as sa

def playsound():
    wave_obj = sa.WaveObject.from_wave_file("/home/pi/Music/se_suc07.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()