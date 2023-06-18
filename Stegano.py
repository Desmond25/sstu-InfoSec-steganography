from tkinter import *
import tkinter.filedialog as fd
from PIL import Image, ImageTk
from stegano import exifHeader
import base64
from base64 import urlsafe_b64encode, urlsafe_b64decode
import chardet

root = Tk()
root.title("Steganography")
root.geometry("1024x570+240+100")
root.resizable(width=False, height=False)
root["bg"] = "LightSteelBlue1"

f_left = Frame(root)
f_right = Frame(root)
f_left.pack(side=LEFT, padx=10)
f_right.pack(side=RIGHT, padx=10)
f_left["bg"] = "LightSteelBlue1"
f_right["bg"] = "LightSteelBlue1"

with open("res/default.txt", 'rb') as file:
                data = file.read().decode('utf-8')

image = Image.open("res/default.jpg")
resizedImage = image.resize((500, 500))
photoImage = ImageTk.PhotoImage(resizedImage)
imgLabel = Label(f_right, image = photoImage)
imgLabel.pack()

imgInTxt = Label(f_left, text="Выберите изображение", anchor='w', bg="LightSteelBlue1")
imgInBtn = Button(f_left, text="Выбрать файл", bg="white")
imgInTxt.pack()
imgInBtn.pack()

fileInTxt = Label(f_left, text="Выберите текстовый документ", anchor='w', bg="LightSteelBlue1")
fileInBtn = Button(f_left, text="Выбрать файл", bg="white")
fileInTxt.pack()
fileInBtn.pack()

pswrdInTxt = Label(f_left, text="Введите пароль", anchor='w', bg="LightSteelBlue1")
pswrdIn = Entry(f_left, show="*", width=30)
pswrdInTxt.pack()
pswrdIn.pack()

crutch = Label(f_left, text = '                                                                                                                                                                        ', 
               anchor = 'w', bg="LightSteelBlue1")
crutch.pack()

encodeBtn = Button(f_left, text="Зашифровать", bg="white")
encodeBtn.pack()

decodeBtn = Button(f_left, text="Расшифровать", bg="white")
decodeBtn.pack()

emptyLabel = Label(f_left, anchor = 'w', bg="LightSteelBlue1")
emptyLabel.pack()

outLabel = Label(f_left, anchor = 'w', bg="LightSteelBlue1")
outLabel.pack()


def OpenImage(event):
    global image
    global photoImage

    imgFilename = fd.askopenfilename(title="Открыть файл", initialdir="/",
                                    filetypes=(("Изображение", "*.jpg *.tiff"),))
    if (imgFilename != ""):
        image = Image.open(imgFilename)
        resizedImage = image.resize((500, 500))
        photoImage = ImageTk.PhotoImage(resizedImage)
        imgLabel.configure(image=photoImage)
        imgLabel.image = photoImage

def OpenFile(event):
    global data

    txtFilename = fd.askopenfilename(title="Открыть файл", initialdir="/",
                                    filetypes=(("Текстовый файл", "*.txt"),))
    if (txtFilename != ""):
        with open(txtFilename, 'rb') as file:
            data = file.read().decode('utf-8')

def Encode(event, image, password, data):
    encodedData = EncodeData(data, password)
    secret = exifHeader.hide(image, "res/secret.jpg", encodedData)
    outLabel.config(text = "Текст был успешно зашифрован.")
    print("Successfully encoded")

def Decode(event, image, password):
    dec = exifHeader.reveal(image)
    dec = dec.decode()
    outLabel.config(text = DecodeData(dec, password))
    print(DecodeData(dec, password))

def EncodeData(data, password):
    return urlsafe_b64encode(bytes(password+data, 'utf-8'))

def DecodeData(enc, password):
    decoded_bytes = base64.urlsafe_b64decode(enc)
    decrypted_str = decoded_bytes.decode('utf-8')

    if password in decrypted_str:
        return decrypted_str.replace(password, '')
    else:
        return 'Ошибка: неправильный пароль.'


imgInBtn.bind("<Button-1>", OpenImage)
fileInBtn.bind("<Button-1>", OpenFile)
encodeBtn.bind("<Button-1>", 
               lambda e: Encode(e, image, pswrdIn.get(), data))
decodeBtn.bind("<Button-1>", 
               lambda e: Decode(e, image, pswrdIn.get()))

root.mainloop()