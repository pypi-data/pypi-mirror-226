import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def load_img(path: str, resize=0.0, recolor=False, greyscale=False):

    """
    It allows to load an image from a path and immediatly apply it some transformations.

    path: The path of the image you want to load.
    resize: It allows to directly resize the image you want to load ( e.g. resize=1.5 -> 150% ). \n        The same resize will be applied to both vertical and horizontal dimensions.
    recolor: It allows to directly recolor the image you want to load. \n        It must be like cv2.COLOR_BGR2RGB , cv2.COLOR_BGR22GRAY, cv2.COLOR_BGR2HSV , ecc.
    greyscale: It allows to directly greyscale recolor the image you want to load. 
    """

    messages=[]

    if not os.path.exists(path):
        raise IOError("File {} does not exist!".format(path))

    if greyscale:
        img1 = cv2.imread(path, 0)
        messages.append("- Greyscale recoloring applied")
    else:
        img1 = cv2.imread(path)

    if resize > 0:
        factor = resize
        img1 = cv2.resize(img1, (0,0), fx=factor, fy=factor) 
        messages.append("- Resize factor applied: {}".format(factor))

    if recolor:
        # cv2.COLOR_BGR2RGB
        img1 = cv2.cvtColor(img1, recolor)
        messages.append("- Color conversion applied: {}".format(str(recolor[4:])))

        
    print("A new image was loaded: {}".format(path))

    for m in messages:
        print(m)

    return img1





def convert_matplotlib_to_opencv_img(matplotlib_format_img: object, clear=False, transitory_img_path='tmp345678.jpg'):

    """
    It allows to convert a matplotlib image into a opencv one.

    matplotlib_format_img: It must be a matplotlib class object, like histograms from function cv2.calcHist.
    clear: If set to true, it will clear any existing matplotlib.pyplot object.
    transitory_img_path: It is just an unlikely filename for the temporary image wich will be created, so that it will not overwrite any file of the user in the working directory.
    """

    messages=[]

    # we can think of plt like an object which "hosts elements" which are "append-plotted" with the method plt.plot.
    # to clean the figure, plt.clf() must be used
    if clear:
        plt.clf()
        messages.append("- The element matplotlib.pyplot was reset ( matplotlib.pyplot.clf() was run )")

    if any(matplotlib_format_img):
        plt.plot(matplotlib_format_img)
        # otherwise it plots the already existing plt
        messages.append("- The input image was added to matplotlib.pyplot")
    else:
        raise IOError("No image was given in input!")

    try:
        plt.savefig(transitory_img_path)

        cv2_imread_format_img = cv2.imread(transitory_img_path)

        import os
        try: 
            os.remove(transitory_img_path)
        except: 
            raise OSError("Could not remove file {}".format(transitory_img_path))

    except: 
        raise OSError("Could not save img to {}".format(transitory_img_path))

    for m in messages:
        print(m)    

    return cv2_imread_format_img



def cyclical_drawing(images: list, labels=[]):

    """
    It allows to display images and videos on VScode.

    Press ESC to close all windows.

    images: list of images you want to display
    labels: list of the labels of the images

    (!) WARNING \n    This function might be very CPU and RAM consuming.    
    """

    if not images:
        raise IOError("No image was given in input!")

    print("--- cyclical drawing --- S")

    # print("images: {}".format(images))

    # labeling
    if not labels:

        labels = []
        for idx, image in enumerate(images):
            labels.append( "my_drawing_" + str(idx+1))
            # only here I make the human friendly index

        # labels = [ "my_drawing_" + str(index()) for image in images ]

    for idx, image in enumerate(images):
        cv2.namedWindow(winname=labels[idx])
        # print( 'my_drawing_'+str(idx) )

    while True:
        for idx, image in enumerate(images):
            cv2.imshow(labels[idx], image)

        if cv2.waitKey(1) & 0xFF == 27: # press esc
            break

    cv2.destroyAllWindows()

    print("--- cyclical drawing --- E")