import cv2
import numpy as np
import sys

def main():
    video_path = getFileName()

    frames = extractFrames(video_path)

    pages = decodeFrames(frames)

    file_path = video_path.replace('.mp4', '_decoded.txt')
    writeToFile(pages, file_path)

def getFileName():
    if len(sys.argv) < 2:
        print("\nError: Video File not provided")
        print("Try 'python encoder.py file_name.mp4'\n")
        sys.exit(1)

    file_name = sys.argv[1]
    
    if(file_name.endswith('.mp4') == False):
       print("\nError: Only .mp4 files are supported!")
       sys.exit(1)
    
    return file_name

def extractFrames(video_path):
    video = cv2.VideoCapture(video_path)

    frames = []

    while(True):
        ret, frame = video.read()

        if(ret):
            frames.append(frame)
        else:
            break

    video.release()
    cv2.destroyAllWindows()

    return frames

def decode(img):
    num_rows = img.shape[0]
    num_cols = img.shape[1]

    data = ''''''

    for row in range(num_rows):
        for col in range(num_cols):
            if(img[row][col] < 127):
                data += '0'
            else:
                data += '1'

    return data

def getIntegerFromBinary(binaryStr = ""):
  return int(binaryStr, 2)

def binaryToText(binaryString):
    textString = ""

    while(len(binaryString) >= 8):
        currentChar = getIntegerFromBinary(binaryString[:8])
        binaryString = binaryString[8:]

        if(currentChar != 255): #Condition for blank trailing part in the image, i.e. when the 8 bit binary string is '11111111'
            textString += chr(currentChar)

    return textString

def decodeFrames(frames):
    pages = []

    for frame in frames:
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #converting 3 Channel image to single channel by grayscale conversion

        binaryData = decode(img)
        page = binaryToText(binaryData)

        pages.append(page)

    return pages

def writeToFile(pages, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        for page in pages:
            file.write(page)

    print("\n\tFile Generated!")

if __name__ == "__main__":
    main()
