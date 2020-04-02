import binascii
import struct
from bitstring import BitArray
from PIL import Image
import math
import numpy as np
import cv2

# I just merged the last 2 assignments and made the code cleaner. It's the same logic as the last 2 assignments

# You just need to change the embeddedFile and carierFile variable with your absolute path and run the script.
# The PSNR and SSIM will be print out in the console.
# Please make sure that the path for the different files are correct for your computer.
# Please install PIL for python3 and opencv (sudo apt-get install python3-opencv)

######################################
#               Embedding
######################################

headerOffset = 1162  # Header size of bmp file : 14 + 124 + 1024 bytes


class Embedding:
    def __init__(self, originFileName, newFileName, hideMsg):
        self.originFileName = originFileName
        self.newFileName = newFileName
        self.hideMsg = hideMsg
        self.bytesCounter = 0  # Function as a pointer
        self.originImageData = ''  # Type: bytes
        self.newImageData = []  # Type: int array

    def openFile(self):
        with open(self.originFileName, 'rb') as fp:
            # Read image file into bytes
            self.originImageData = fp.read()

    def copyHeader(self):
        # Read bmp file header (14) and bitmap info header (124) and palette (1024)
        # Copy them into new image
        for i in range(0, headerOffset):
            self.newImageData.append(self.originImageData[i])
            self.bytesCounter += 1

    def hideInt(self, currHideInt):
        currHideBin = '{:032b}'.format(currHideInt)
        for i in range(0, 32):
            currImageBin = '{0:08b}'.format(self.originImageData[self.bytesCounter])
            # In little endian mode, LSB is the first bit
            newImageBin = currHideBin[i] + currImageBin[1:]
            newImageInt = int(newImageBin, 2)
            self.newImageData.append(newImageInt)
            self.bytesCounter += 1

    def hideChar(self, currHideByte):
        # ord(): convert char to int
        # Then get binary value of one byte
        # Example:
        # a = '{0:08b}'.format(255)
        # print(a) # '1111111'
        currHideBin = '{0:08b}'.format(ord(currHideByte))

        # Hide one byte in eight bytes
        for i in range(0, len(currHideBin)):
            currImageBin = '{0:08b}'.format(self.originImageData[self.bytesCounter])
            # In little endian mode, LSB is the first bit
            newImageBin = currHideBin[i] + currImageBin[1:]
            newImageInt = int(newImageBin, 2)
            self.newImageData.append(newImageInt)
            self.bytesCounter += 1

    def hide(self):
        # Hide length of message
        self.hideInt(len(self.hideMsg))
        # Hide message byte by byte
        for i in range(0, len(self.hideMsg)):
            self.hideChar(self.hideMsg[i])

    def copyRemain(self):
        # Copy rest data into new image
        leftData = self.originImageData[self.bytesCounter:]
        for left_byte in leftData:
            self.newImageData.append(left_byte)

    def writeNewBmp(self):
        with open(self.newFileName, 'wb') as outputFile:
            new_image_bytes = bytearray(self.newImageData)
            outputFile.write(new_image_bytes)

    def embed(self):
        self.openFile()
        self.copyHeader()
        self.hide()
        self.copyRemain()
        self.writeNewBmp()


textFile = 'Python/Assign05/Declaration_of_Independence.txt'
file2embed = open(textFile, 'r')
text2embed = file2embed.read()
file2embed.close()

embeddedFile = '/home/aurelien/Documents/IIT/stegano/Steganography/Python/Assign05/ballons_rgb_embedded.bmp'
carierFile = '/home/aurelien/Documents/IIT/stegano/Steganography/Python/Assign05/ballons_rgb.bmp'
encryption = Embedding(carierFile, embeddedFile, text2embed)
encryption.embed()


######################################
#               Retrieving
######################################

class Retrieving:

    def __init__(self, newFileName):
        self.newFileName = newFileName
        self.fp = open(self.newFileName, 'rb')
        self.hiddenMsg = ''

    def readHeader(self):
        for i in range(0, headerOffset):
            self.fp.read(1)

    def getInt(self):
        currHideBin = ''

        for i in range(0, 32):
            currImageByte = self.fp.read(1)
            if len (currImageByte) == 0:
                return ''
            currImageBin = '{0:08b}'.format(ord(currImageByte))
            currHideBin += currImageBin[0]

        currHideInt = int(currHideBin, 2)
        return currHideInt

    def getChar(self):
        currHideBin = ''

        for i in range(0, 8):
            currImageByte = self.fp.read(1)
            if len(currImageByte) == 0:
                return ''
            currImageBin = '{0:08b}'.format(ord(currImageByte))
            currHideBin += currImageBin[0]
        currHideChar = chr(int(currHideBin, 2))
        return currHideChar
    
    def retrieveMsg(self):
        currHideInt = self.getInt()
        for i in range(0, currHideInt):
            currHideChar = self.getChar()
            self.hiddenMsg += currHideChar
        self.fp.close()

    def retrieve(self):
        self.readHeader()
        self.retrieveMsg()
        return self.hiddenMsg


secretMsg = 'Python/Assign05/secret_msg.txt'
fileMsg = open(secretMsg, 'w')
decryption = Retrieving(embeddedFile)
fileMsg.write(decryption.retrieve())
fileMsg.close()


######################################
#               Analysis
######################################

def calculate_psnr(img1, img2):
    # img1 and img2 have range [0, 255]
    image1 = Image.open(img1)
    image1.load()
    buffer1 = np.asarray_chkfinite(image1, dtype="int32")
    image2 = Image.open(img2)
    image2.load()
    buffer2 = np.asarray_chkfinite(image2, dtype="int32")
    img1 = buffer1.astype(np.float64)
    img2 = buffer2.astype(np.float64)
    mse = np.mean((img1 - img2)**2)
    if mse == 0:
        return float('inf')
    return 20 * math.log10(255.0 / math.sqrt(mse))

psnr = calculate_psnr(embeddedFile, carierFile)

print("PSNR: " + str(psnr))


def ssim(img1, img2):
    C1 = (0.01 * 255)**2
    C2 = (0.03 * 255)**2

    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    kernel = cv2.getGaussianKernel(11, 1.5)
    window = np.outer(kernel, kernel.transpose())

    mu1 = cv2.filter2D(img1, -1, window)[5:-5, 5:-5]  # valid
    mu2 = cv2.filter2D(img2, -1, window)[5:-5, 5:-5]
    mu1_sq = mu1**2
    mu2_sq = mu2**2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = cv2.filter2D(img1**2, -1, window)[5:-5, 5:-5] - mu1_sq
    sigma2_sq = cv2.filter2D(img2**2, -1, window)[5:-5, 5:-5] - mu2_sq
    sigma12 = cv2.filter2D(img1 * img2, -1, window)[5:-5, 5:-5] - mu1_mu2

    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) *
                                                            (sigma1_sq + sigma2_sq + C2))
    return ssim_map.mean()


def calculate_ssim(img1, img2):
    '''calculate SSIM
    the same outputs as MATLAB's
    img1, img2: [0, 255]
    '''
    image1 = Image.open(img1)
    image1.load()
    buffer1 = np.asarray_chkfinite(image1, dtype="int32")
    image2 = Image.open(img2)
    image2.load()
    buffer2 = np.asarray_chkfinite(image2, dtype="int32")
    if not buffer1.shape == buffer2.shape:
        raise ValueError('Input images must have the same dimensions.')
    if buffer1.ndim == 2:
        return ssim(buffer1, buffer2)
    elif buffer1.ndim == 3:
        if buffer1.shape[2] == 3:
            ssims = []
            for i in range(3):
                ssims.append(ssim(buffer1, buffer2))
            return np.array(ssims).mean()
        elif buffer1.shape[2] == 1:
            return ssim(np.squeeze(buffer1), np.squeeze(buffer2))
    else:
        raise ValueError('Wrong input image dimensions.')

ssim = calculate_ssim(embeddedFile, carierFile)
print("SSIM: " + str(ssim))

