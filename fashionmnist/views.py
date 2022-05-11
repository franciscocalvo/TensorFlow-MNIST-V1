import pathlib
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import tensorflow as tf
from django.core.files import File
from pathlib import Path
import os
from PIL import Image
import PIL.ImageOps
import numpy as np
from django import forms

class UploadFileForm(forms.Form):
    img = forms.FileField()

def index(request):
    return render(request,'index.html')

def upload(request):
    
    proyectPath = os.path.dirname(__file__)
    fileModel = proyectPath+"/static/Model/fashion_mnist"
    new_model = tf.keras.models.load_model(fileModel)

    if request.method == 'POST' and request.FILES['imagen']:
        upload = request.FILES['imagen']
        fss = FileSystemStorage()

        file = fss.save(upload.name,upload)

        
            
        img = Image.open(file)  #aqui introduccimos la ruta de la imagen
        imgGray = img.convert('L')
        imgGray.save(proyectPath+'/static/img/imagen_b_n.png')

            #invertir los colores de la imagen
        image = Image.open(proyectPath+'/static/img/imagen_b_n.png')
        inverted_image = PIL.ImageOps.invert(image)
        inverted_image.save(proyectPath+'/static/img/imagen_b_n_i.png')
        os.remove(proyectPath+'/static/img/imagen_b_n.png')

            #cambiamos la resolucion de la imagen a 28*28
        img = Image.open(proyectPath+'/static/img/imagen_b_n_i.png')
        new_img = img.resize((28,28))
        new_img.save(proyectPath+'/static/img/imagen_b_n_i_r.png','png')
        os.remove(proyectPath+'/static/img/imagen_b_n_i.png')

        img = Image.open(proyectPath+"/static/img/imagen_b_n_i_r.png")
        img.load()
        img = (np.expand_dims(img,0))
        predictions_single = new_model.predict(img/255)

        funcion = np.argmax(predictions_single[0])

        if funcion == 0:
            mensaje='La imagen es un Camiseta'
        elif funcion == 1:
            mensaje='La imagen es un Pantalones'
        elif funcion == 2:
            mensaje='La imagen es un Sudadera/Remera'
        elif funcion == 3:
            mensaje='La imagen es un Vestido'
        elif funcion == 4:
            mensaje='La imagen es un Abrigo/Chaquetón'
        elif funcion == 5:
            mensaje='La imagen es un Chanclas'
        elif funcion == 6:
            mensaje='La imagen es un Camisa'
        elif funcion == 7:
            mensaje='La imagen es un Deportivas'
        elif funcion == 8:
            mensaje='La imagen es un Mochila/Bolso'
        elif funcion == 9:
            mensaje='La imagen es un Botines/Botas'
        else:
            mensaje='No se encontró ninguna coincidencia'

    
    os.remove(upload.name)
    os.remove(proyectPath+"/static/img/imagen_b_n_i_r.png")
    return render(request,'prediction.html',{'mensaje':mensaje})