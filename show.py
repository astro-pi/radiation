from astro_pi import AstroPi
ap = AstroPi()

def draw(rate,subtracted):
        ap.show_message(str(rate), scroll_speed=1, text_colour=[255,0,0]) # red for count rate
        ap.show_message(str(subtracted), scroll_speed=1, text_colour=[0,0,255]) #blue for faulty/noisy pixels
def calibrateMessage():
    ap.show_letter("C")