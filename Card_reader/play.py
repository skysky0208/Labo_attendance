import simpleaudio as sa

def playsound():
    wave_obj = sa.WaveObject.from_wave_file("/home/pi/Music/success.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()

def playerrorsound():
    wave_obj = sa.WaveObject.from_wave_file("/home/pi/Music/error.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()
    
