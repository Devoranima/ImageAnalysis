from PIL import Image, ImageFilter
#import os 

#def get_imlist(path):
#  return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]


#filelist = get_imlist('./')
#for infile in filelist:
#  outfile = os.path.splitext(infile)[0] + ".jpg"
#  if infile!= outfile:
#    try:
#      Image.open(infile).save(outfile)
#    except IOError:
#      print("cannot convert", infile)

img = Image.open("image.jpg")
img2 = img.filter(ImageFilter.EMBOSS)
img2.show()

