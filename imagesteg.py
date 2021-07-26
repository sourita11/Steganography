import PIL.Image #pip install pillow
import cv2  #pip install opencv-python
import sys

import tkinter


from tkinter import *

def popupmsg(msg,data=""):
    fullmessage = msg+data
    popup = tkinter.Tk()
    popup.configure(bg = "White")
    popup.geometry("700x100")
    popup.wm_title("!")
    label = tkinter.Label(popup, text=fullmessage)
    label.pack(side= TOP, fill="x", pady=10)
    popbutton = tkinter.Button(popup, text="Okay", command = popup.destroy, bg = "Green" , fg = "White")
    popbutton.pack()
    popup.mainloop()    


def encodemenu():
    encodewindow = tkinter.Toplevel(root) #new window
    encodewindow.geometry("600x400")
    encodelabel = tkinter.Label(encodewindow, text =
   "\n___________________________________________________\n\
      |                         ENCODING                             |\
    \n| INFO: Specify an image & the data to be encoded: |", bg = "White").pack(side = TOP)
    
    imglabel = Label(encodewindow, text = "ENTER FULL IMAGE PATH(with extension):").place(x=20, y=100)
    imgentry = Entry(encodewindow, bd = 5, textvariable = imgvar).place(x=375, y=100)
    
    
    datalabel = Label(encodewindow, text = "ENTER DATA TO BE ENCODED :").place(x=20, y=130)
    dataentry = Entry(encodewindow, bd = 5, textvariable = datavar).place(x=375, y=130)
    

    newimglabel = Label(encodewindow, text = "ENTER FULL IMAGE PATH FOR ENCODED IMAGE(with extension):").place(x=20, y=160)
    newimgentry = Entry(encodewindow, bd = 5, textvariable = newimgvar).place(x=375, y=160)
    
    
    encodebutton = tkinter.Button(encodewindow,text = 'Encode', command = encodesubmit, bg = "Blue" , fg = "White" ).place(x=350, y=200)
    gobackbutton = tkinter.Button(encodewindow,text = 'Go back', command = encodewindow.destroy, bg = "Blue" , fg = "White" ).place(x=400, y=200)

    
def decodemenu():
    decodewindow = tkinter.Toplevel(root) #new window
    decodewindow.geometry("600x300")
    decodelabel = tkinter.Label(decodewindow, text =
    "\n___________________________________________________\n\
      |                         DECODING                             |\
    \n| INFO: Specify an encoded image to extract data : |", bg = "White").pack(side = TOP)
    
    imglabel = Label(decodewindow, text = "ENTER FULL IMAGE PATH TO DECODE(with extension):").place(x=20, y=130)
    imgentry = Entry(decodewindow, bd = 5, textvariable = decodeimgvar).place(x=375, y=130)
    
    
    decodebutton = tkinter.Button(decodewindow,text = 'Decode', command = decodesubmit, bg = "Blue" , fg = "White" ).place(x=350, y=170)
    gobackbutton = tkinter.Button(decodewindow,text = 'Go back', command = decodewindow.destroy, bg = "Blue" , fg = "White" ).place(x=400, y=170)

def checkmenu():
    
    checkwindow = tkinter.Toplevel(root) #new window
    checkwindow.geometry("600x500")
    checklabel = tkinter.Label(checkwindow, text =
   "\n___________________________________________________\n\
      |                         CHECKING                             |\
    \n| INFO: Specify any two images to compare: |" , bg = "White").pack(side = TOP)
    
    imglabel1 = Label(checkwindow, text = "ENTER FIRST IMAGE PATH(with extension):").place(x=20, y=100)
    imgentry1 = Entry(checkwindow, bd = 5, textvariable = checkvar1).place(x=375, y=100)
    
    
    imglabel2 = Label(checkwindow, text = "ENTER SECOND IMAGE PATH(with extension):").place(x=20, y=130)
    imgentry2 = Entry(checkwindow, bd = 5, textvariable = checkvar2).place(x=375, y=130)

    
    checkbutton = tkinter.Button(checkwindow,text = 'Check', command = checksubmit, bg = "Blue" , fg = "White" ).place(x=350, y=200)
    gobackbutton = tkinter.Button(checkwindow,text = 'Go back', command = checkwindow.destroy , bg = "Blue" , fg = "White").place(x=400, y=200)
    
def encodesubmit(): 
  
    img = imgvar.get() 
    data = datavar.get()
    new_img = newimgvar.get()
    if (img == "" or data == "" or new_img == ""):
        popupmsg("ENTRY FIELDS CANNOT BE EMPTY !!")
    else:
        encode(img, data, new_img)
      
    imgvar.set("") 
    datavar.set("")
    newimgvar.set("")

def decodesubmit(): 
  
    dimg = decodeimgvar.get()
    if (dimg == ""):
        popupmsg("FIELD CANNOT BE EMPTY !!")
    else:
        decode(dimg)
      
    decodeimgvar.set("")

def checksubmit():

    img1 = checkvar1.get()
    img2 = checkvar2.get()
    if (img1 == "" or img2 == ""):
        popupmsg("ENTRY FIELDS CANNOT BE EMPTY !!")
    else:
        check(img1, img2)

    checkvar1.set("")
    checkvar2.set("")


    
def encode(img, data, new_img):
        
    try:
        image = PIL.Image.open(img , 'r')
            
                
        copy_img = image.copy() #creating copy to work on
                
                
        datalist = []
            
        for i in data:
            datalist.append(format(ord(i),'08b'))
                                
        datalen = len(datalist) 
        pixiter = iter(copy_img.getdata())  #list of pixel line by line

        pixellist=[] #storing new pixels here      

            #encoding here                   
        for i in range(datalen):
                
            pixel = [value for value in next(pixiter)[:3]+ next(pixiter)[:3] + next(pixiter)[:3]]
                        
                #changing pixel values
                #odd for 1 , even for 0                        
            for j in range(8):
                if (datalist[i][j] == '0' and pixel[j]%2 != 0):
                        #binary value of data is 0 and existing
                                #pixel is odd then make it even
                    pixel[j]-=1
                        
                elif (datalist[i][j] == '1' and pixel[j]%2 == 0):
                        #binary is 1 and pixel is even then change to odd
                    pixel[j]+=1
                        
                #end of j loop
                                             
                #whether to stop or read further at 9th bit
                #even to continue odd to stop
                #if even set to odd 
            if(i == (datalen -1)):
                    #reached last bit
                if (pixel[-1]%2==0):  #even so set to odd
                    if(pixel[-1]!=0):
                        pixel[-1]-=1
                    else:
                        pixel[-1]+=1
            else:  #not reached end so set last bit to even
                if (pixel[-1]%2 != 0):
                    pixel[-1]-=1

                #replacing pixels
            new_pixel = tuple(pixel)
                
            (pix1,pix2,pix3) = (tuple(new_pixel[0:3]),tuple(new_pixel[3:6]),tuple(new_pixel[6:9]))
                 
                
            pixellist.append(pix1)
            pixellist.append(pix2)
            pixellist.append(pix3)
                

            #end of i loop
        copy_img.putdata(pixellist)
               
            #saving encoded image
        popupmsg("ENCODING SUCCESSFUL...ENCODED IMAGE SAVED SUCCESSFULLY !!")
            
            
        copy_img.save(new_img, str(new_img.split(".")[1].upper()))
            
    except:
        popupmsg("ERROR!! FILE NOT FOUND! PLEASE TRY AGAIN")

        
    
def decode(img):


    try:
        image = PIL.Image.open(img, 'r')
                
        data = '' #entire data in list
        pixiter = iter(image.getdata())
        
        while True:
            #extracting 3 pixels at a time - 8 bit data 9th bit indicator
            pixel = [value for value in next(pixiter)[:3]+ next(pixiter)[:3] + next(pixiter)[:3]]

            binstr = '' #storing bin value
            for i in (pixel[:8]):
                if (i%2 == 0): #if even append 0
                    binstr+='0'
                else: #if odd append 1
                    binstr+='1'

            data+= chr(int(binstr,2)) #append converted char to data
            if (pixel[-1]%2 != 0): #if odd data is over
                return popupmsg("DECODING SUCCESSFUL...\nDECODED DATA =>   ",data)
    except:
        popupmsg("ERROR!! FILE NOT FOUND! PLEASE TRY AGAIN")

def check(img1, img2):
    #to check if images are equal
    
    try:
        original = cv2.imread(img1)
        duplicate = cv2.imread(img2)
    
        
        difference = cv2.subtract(original,duplicate) #difference in BGR pixels
        b, g, r = cv2.split(difference)
        
                
        if(original.shape == duplicate.shape):
            if(cv2.countNonZero(b) == 0 and cv2.countNonZero(g)== 0 and cv2.countNonZero(r) ==0): #gives height, width, channels(b,g,r)
                popupmsg("THE IMAGES HAVE SAME SIZE AND NUMBER OF CHANNELS AND THEY ARE COMPLETELY EQUAL")
            else:
                popupmsg("THE IMAGES HAVE SAME SIZE AND NUMBER OF CHANNELS BUT THEY ARE NOT COMPLETELY EQUAL")
        else:
            popupmsg("THE IMAGES DO NOT HAVE SAME SIZE AND NUMBER OF CHANNELS")
            
    except:
        popupmsg("ERROR !! FILE NOT FOUND ! PLEASE TRY AGAIN ")
                    
            
root = tkinter.Tk()
root.title("IMAGE STEGANOGRAPHY")
root.geometry("600x300")

imgvar = tkinter.StringVar()
datavar = tkinter.StringVar()
newimgvar = tkinter.StringVar()
decodeimgvar = tkinter.StringVar()
checkvar1 = tkinter.StringVar()
checkvar2 = tkinter.StringVar()

mainlabel = Label(root,text ="|------------------------------------------------ WELCOME TO STEGANOGRAPHY -----------------------------------------------|\n\n|\t\t\tFastest way of disguising data into an image\t\t\t\t|\n", bg = "White")
menulabel = Label(root,text = "\n CHOOSE YOUR OPTION \n",bg = "Cyan")
      
mainlabel.pack(side = TOP)
menulabel.pack(side = TOP)


Bencode = tkinter.Button(root, text = "ENCODE", command = encodemenu, bg = "Black", fg = "White" ).place(x = 170, y = 130)
Bdecode = tkinter.Button(root, text = "DECODE", command = decodemenu, bg = "Black", fg = "White" ).place(x = 245, y = 130)
Bcheck = tkinter.Button(root, text = "CHECK", command = checkmenu, bg = "Black", fg = "White" ).place(x = 320, y = 130)
Bexit = tkinter.Button(root, text = "EXIT", command = root.destroy, bg = "Black", fg = "White" ).place(x = 395, y = 130)
      
root.mainloop()
