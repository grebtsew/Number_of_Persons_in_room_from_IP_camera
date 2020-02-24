from Xlib.display import Display
screen = Display(':0').screen()
print(screen.width_in_pixels, screen.height_in_pixels)
