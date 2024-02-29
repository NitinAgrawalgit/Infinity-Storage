import cv2
import numpy as np
import sys

def main():
    num_rows = 240 #Defining Resolution (240p)
    num_cols = 320

    file_path = getFileName()

    pages = readFile(num_rows, num_cols, file_path)

    frames = createFrames(pages, num_rows, num_cols)

    video_path = file_path.replace('.txt', '.mp4')
    frame_rate = 4
    compileVideo(frames, video_path, frame_rate)

def getFileName():
    if len(sys.argv) < 2:
        print("\nError: Text File not provided")
        print("Try 'python encoder.py file_name.txt'\n")
        sys.exit(1)

    file_name = sys.argv[1]
    
    if(file_name.endswith('.txt') == False):
       print("\nError: Only .txt files are supported!")
       sys.exit(1)

    return file_name

def initImage(num_rows, num_cols):
    img = np.empty((num_rows, num_cols), dtype = np.uint8) #np.uint8 instead of just int, bcz cv2.VideoWriter needs this type

    #Creating empty Image
    for i in range(num_rows):
        for j in range(num_cols):
            img[i][j] = 255

    return img

def encode(img, data):
    num_rows = img.shape[0]
    num_cols = img.shape[1]

    i = 0
    contentLength = len(data)

    for row in range(num_rows):
        for col in range(num_cols):
            if i >= contentLength:
                return img

            if(data[i] == '0'):
                img[row][col] = 0
            else:
                img[row][col] = 255

            i += 1

    return img

def textToBinary(textString):
    binary_string = ''.join(format(ord(i), '08b') for i in textString)
    return binary_string

def readFile(num_rows, num_cols, file_path):
    chars_per_page = int((num_rows * num_cols) / 8)

    pages = []

    with open(file_path, "r", encoding="utf-8") as file:
        while True:
            page = file.read(chars_per_page)
            if not page:
                break

            pages.append(page)

    return pages

def createFrames(pages, num_rows, num_cols):
    frames = []

    for page in pages:
        binaryData = textToBinary(page)
        img = initImage(num_rows, num_cols)
        img = encode(img, binaryData)

        frames.append(img)

    return frames

def compileVideo(frames, video_path, frame_rate):
    frame_size = [frames[0].shape[1], frames[0].shape[0]]
    cv2_fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    video = cv2.VideoWriter(video_path, cv2_fourcc, frame_rate, frame_size, isColor=False)

    for frame in frames:
        video.write(frame)

    video.release()

    print("\n\tVideo File Generated!")

if __name__ == '__main__':
    main()