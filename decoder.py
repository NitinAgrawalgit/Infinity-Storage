import numpy as np
import cv2

def main():
    file_name = 'harry_potter_yt' #FILE NAME TO BE ENTERED HERE
    video_path = '../videos/' + file_name + '.mp4'

    frames = extractFrames(video_path)

    pages = decodeFrames(frames)

    file_path = '../textfiles_result/' + file_name + '.txt'
    writeToFile(pages, file_path)

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
