from cgitb import text
import shutil
from PIL import Image
import os
import pyperclip


##### variables y constantes #####
COORDENATES = [(1, 1, 513, 513), (511, 1, 1023, 513), (1, 511, 513, 1023), (511, 511, 1023, 1023)]
IMAGES_FOLDER = input(" - Path of images to crop: ")
SAVE_FOLDER = input(" - Path to save crop images: ")

while os.path.exists(SAVE_FOLDER):
    print("\n - THE SAVE FOLDER ALREADY EXISTS")
    option = input("\n - Wanna u rewrite it? (y/n): ")
    if option.lower() == "y":
        shutil.rmtree(SAVE_FOLDER)
        os.mkdir(SAVE_FOLDER)
        break
    else:
        print("\n - SELECT ANOTHER SAVE PATH FOLDER: ")
        SAVE_FOLDER = input("\n - Path to save images: ")

print("\n\t Path correctly selected...\n")
        


########## FUNCIONES ##############
# funcion para ver si el archivo pasado por parametro es .png
def image_test(img):
    return (os.path.splitext(img)[1] == ".jpg" or os.path.splitext(img)[1] == ".png" 
    or os.path.splitext(img)[1] == ".bmp" or os.path.splitext(img)[1] == ".tga")

def return_only_name(file):
    return os.path.splitext(file)[0]

# funcion para cortar cada coordenada de una imagen pasada por parametro
def cut_image(image, path):
    # abrir la imagen
    image_open = Image.open(path+ "/" +image)
    # cortar
    if image_open.size == (2048,2048):
        image_open = resize(image_open)

    # guardar los cortes
    cuts = []
    # por cada coordenada, cortar la imagen en esa coordeanda
    for every_coordenate in COORDENATES:
        cuts.append(image_open.crop(every_coordenate))
    return cuts

def resize(image):
        return image.resize((1024,1024))

def non_edited(image):
        return image[-1] != '1' and image[-1] != '2' or image[-1] != '3' or image[-1] != '4'
########################################

# ver todos los archivos en el directorio pasado
files_in_folder = os.listdir(IMAGES_FOLDER)
# para cada archivo en la lista de files_in_folder vemos cuales son imagenes
images_in_folder = list(filter(image_test, files_in_folder))

# solo las imagenes NO editadas, osea no tienen _topleft, _topright... etc
images_non_edited = list(filter(non_edited,images_in_folder))
# images_in_folder esun listado de las imagenes nomas

def start_cutting(images_in_folder):
    if (len(images_in_folder) == 0):
        print("THERE ISN'T IMAGES TO EDIT!!!")
        return 0
    print("\n - Processing images and cutting it...- \n")
    for each_image in images_in_folder:
        cuttes = cut_image(each_image,IMAGES_FOLDER)
        index = 0
        for each_cut_of_the_image in cuttes:
            index += 1
            each_cut_of_the_image.save(SAVE_FOLDER+"/"+return_only_name(each_image)+str(index)+".bmp", quality=100)
        
if __name__ == "__main__":
    start_cutting(images_non_edited)
    images_saved = os.listdir(SAVE_FOLDER)
    images_order = [[], [], [], [], [], [], [],[]]
    first = 0
    for images in images_saved:
            if images.find("lf") != -1:
                images_order[1].append(images)
            elif images.find("rt")!= -1:
                images_order[2].append(images)
            elif images.find("up")!= -1:
                images_order[3].append(images)
            elif images.find("bk")!= -1:
                images_order[4].append(images)
            elif images.find("rt")!= -1:
                images_order[5].append(images)
            elif images.find("dn") != -1:
                images_order[6].append(images)
            elif images.find("ft") != -1:
                if images.find("ft4") != -1:
                    images_order[0].append(images)
                else:
                    images_order[7].append(images)

    text = '{ '
    for image_ordered in images_order:
        for image_individual in image_ordered:
            text += '"'+ image_individual + '" '
    text += '}'

    print(f"\n ---------------------- \n \t COMPLETED \nIMAGES SAVED ARE 24-32 BITS DEPTH | \t REMEMBER CONVERT TO 8 BITS DEPTH !!!\n \n - {text} \n -------------------------------- \n")
    option = input("\n Copy to clipboard (press Y for YES and exit/press N for NO and exit): ")

    if option.lower() == "y":
        pyperclip.copy(text)
        print("\n Copied")
    else:
        pass

    exit()
