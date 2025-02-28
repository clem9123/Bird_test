from PIL import Image, ImageTk

def charger_image(filepath, height=None):
    image = Image.open(filepath)
    if height:
        ratio = height / float(image.size[1])
        width = int(image.size[0] * ratio)
        image = image.resize((width, height), Image.LANCZOS)
    return ImageTk.PhotoImage(image)
