import imghdr
import subprocess


def infoBMPImage(image):
    imageType = imghdr.what(image) # library used to chek bmp file: https://docs.python.org/3.6/library/imghdr.html
    infoDict = {}
    exifToolPath = 'exiftool' # command to read the meta data of an image: https://exiftool.org/ 

# print(imageType)

    if (imageType == 'bmp'):
       print("Your image is a BMP file!")

    else:
     print("Please provide a BMP file")

    # use Exif tool to get the metadata 
    process = subprocess.Popen([exifToolPath,image],stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True) # Pipe and redirection to store tha data
    # get the tags in dict
    for tag in process.stdout:
        line = tag.strip().split(':')
        infoDict[line[0].strip()] = line[-1].strip()

    if (infoDict["BMP Version"] == "Windows V5"):
        print("Your DIB Header version is BITMAPV5HEADER!")
    else:
        print("Your DIB Header version is: " + infoDict["BMP Version"] + ", it\'s not the correct version!") # Header info: 
                                                                                                             # https://en.wikipedia.org/wiki/BMP_file_format#Bitmap_file_header
                                                                                                             # https://docs.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-bitmapv5header

    # Another solution would have been to read the data with open(image, 'rb') (the first one I use): 
    # Then to store the file in a string and iterate within this string with the offset:
    # bufferInfo[0xXX] with XX = offset given by the documentation and bufferInfo = BMPfile.read() (cf writeBMP function);
    # But the solution with the exiftool command make it more simple to read the data aftermath.
    
    print("The file size is: " + infoDict["File Size"])
    print("The image dimensions are: {0}x{1}".format(infoDict["Image Width"], infoDict["Image Height"]))
                                                                                                    
def writeNewBMP(imageSource):
    inputImage = open(imageSource, 'rb')
    bufferInfo = inputImage.read()
    inputImage.close()

    outputImage = open('Python/Assign04/output_image.bmp', 'wb')
    outputImage.write(bufferInfo)
    outputImage.close()
    


infoBMPImage('Python/Assign04/ballons_rgb.bmp')
writeNewBMP('Python/Assign04/ballons_rgb.bmp')
