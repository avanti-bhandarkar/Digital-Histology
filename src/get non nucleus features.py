#Import libraries
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image  
import pandas as pd

#Define a function to convert RGB (Red, Blue, Green) to HSV (Hue, Saturation, Value) colourspace 
def rgb_to_hsv(r, g, b):
    maxc = max(r, g, b) # Extract maximum red,blue and green values from the image
    minc = min(r, g, b) # Extract minimum red,blue and green values from the image
    v = maxc # Set value equal to maximum RGB value
    if minc == maxc: # If maximum and minimum values are equal, set hue and saturation value to 0
        return 0.0, 0.0, v
    s = (maxc-minc) / maxc # Set saturation value to the ratio rgb range and maximum rgb value
    # Initialise red, blue and green channels in terms of maximum/minimum values and inputs to the function
    rc = (maxc-r) / (maxc-minc)
    gc = (maxc-g) / (maxc-minc)
    bc = (maxc-b) / (maxc-minc)
    # Define hue values using an else-if ladder as per the formulae used here (https://www.rapidtables.com/convert/color/rgb-to-hsv.html)
    if r == maxc:
        h = bc-gc
    elif g == maxc:
        h = 2.0+rc-bc
    else:
        h = 4.0+gc-rc
    h = (h/6.0) % 1.0
    return h, s, v

#Define a function to obtain HSV color from the loaded image
def HSVColor(img):
    if isinstance(img,Image.Image): # The code below is only executed if the image has been loaded using PIL
        r,g,b = img.split() # Split the RGB image into constituent channels
        # Initialise empty lists for HSV values
        Hdat = [] 
        Sdat = []
        Vdat = [] 
        for rd,gn,bl in zip(r.getdata(),g.getdata(),b.getdata()) : # Get pixel values for rgb channels from the images and zip them
            h,s,v = rgb_to_hsv(rd/255.,gn/255.,bl/255.) # Apply previouslty defined rgb_to_hsv function and append the values obtained into the blank lists
            Hdat.append(int(h*255.))
            Sdat.append(int(s*255.))
            Vdat.append(int(v*255.))
        # Copy HSV values pixelwise to form 3 channels
        r.putdata(Hdat)
        g.putdata(Sdat)
        b.putdata(Vdat)
        # Merge the 3 channels obtained in the previous step to get a complete HSV image
        return Image.merge('RGB',(r,g,b))
    else:
        return None
    
print('Loading image ...\n')
#Load image in PIL (for RGB and HSV features)
nonucleus_region = Image.open("/Users/avantibhandarkar/Desktop/digital histopathology/op images/nonucleus_region.png")
#Load image in OpenCV (for LAB features)
nonucleus_regions = cv2.imread("/Users/avantibhandarkar/Desktop/digital histopathology/op images/nonucleus_region.png")

print('Extracting RGB features ...')
#Get RGB features
imgrgb_nonu = nonucleus_region.copy()#Make a copy of the loaded image
RGB_nonu = list(imgrgb_nonu.getdata())#Get pixelwise RGB values for the images
RGB_nonu = np.array(RGB_nonu)#Store obtained values as an array
print('Shape of the RGB feature matrix is',np.shape(RGB_nonu))
df_RGB_nonu = pd.DataFrame(RGB_nonu, columns = ['R','G','B'])#Convert the array into a dataframe and save it as a csv file 
df_RGB_nonu.to_csv('/Users/avantibhandarkar/Desktop/digital histopathology/csv files/RGB_nonu.csv', index=False)

print('\nExtracting HSV features ...')
#Get HSV features
imghsv_nonu = nonucleus_region.copy()#Make a copy of the loaded image
imghsv_final_nonu = HSVColor(imghsv_nonu)#Convert from RGB to HSV colourspace
HSV_nonu = list(imghsv_final_nonu.getdata())#Get pixelwise HSV values for the images
HSV_nonu = np.array(HSV_nonu)#Store obtained values as an array
print('Shape of the HSV feature matrix is',np.shape(HSV_nonu))
df_HSV_nonu = pd.DataFrame(HSV_nonu,columns = ['H','S','V'])#Convert the array into a dataframe and save it as a csv file 
df_HSV_nonu.to_csv('/Users/avantibhandarkar/Desktop/digital histopathology/csv files/HSV_nonu.csv', index=False)

print('\nExtracting LAB features ...')
#Get LAB features
imglab_nonu = cv2.cvtColor(nonucleus_regions,cv2.COLOR_RGB2Lab) #convert from RGB to LAB using OpenCV inbuilt function
cv2.imwrite('/Users/avantibhandarkar/Desktop/digital histopathology/op images/imglab_nonu.jpg',imglab_nonu)#Save the obtained image
imglab_final_nonu = Image.open("/Users/avantibhandarkar/Desktop/digital histopathology/op images/imglab_nonu.jpg") #Open the image (saving and reopening an image helps convert LAB values into a format that can be used up by the .getdata() function)
LAB_nonu = list(imglab_final_nonu.getdata())#Get pixelwise LAB values for the images
LAB_nonu = np.array(LAB_nonu)#Store obtained values as an array
print('Shape of the LAB feature matrix is',np.shape(LAB_nonu))
df_LAB_nonu = pd.DataFrame(LAB_nonu, columns = ['L','A','B'])#Convert the array into a dataframe and save it as a csv file 
df_LAB_nonu.to_csv('/Users/avantibhandarkar/Desktop/digital histopathology/csv files/LAB_nonu.csv', index=False)

print('\nGenerating feature matrix for region with no nuclei ...')
nonucleus = np.hstack((RGB_nonu , HSV_nonu , LAB_nonu))
print('Shape of the no-nucleus feature matrix is',np.shape(nonucleus))#Horizontally stack the 3 arrays to get a (rows,9) matrix representing all the no-nucleus features)
np.save('/Users/avantibhandarkar/Desktop/digital histopathology/npy files/nonucleus_features.npy', nonucleus) #save the obtained array as an .npy file for future use
