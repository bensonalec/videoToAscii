import time, sys, click, ffmpeg
from PIL import Image
from os import system

toWait = 0
def parseFrames(inputVid):
    probe = ffmpeg.probe(inputVid)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    width = int(video_stream['width'])
    height = int(video_stream['height'])
    length = float(video_stream['duration'])

    
    iter = length / 720
    toWait = iter
    total = 0
    
    for  i in range(360):
        im = "./Frames/im" + str(i) + ".png"
        out = "./Frames/out" + str(i) + ".png"
        total += iter
        (
            ffmpeg
            .input(inputVid, ss=total)
            .filter('scale', width/8, -1)
            .output(im, vframes=1)
            .run()
        )

def detAscii(gray, freq):
    if(gray == freq):
        return "-"
    elif(gray >= 230):
        return " "
    elif(gray >= 200):
        return "."
    elif(gray >= 180):
        return "*"
    elif(gray >= 160):
        return ":"
    elif(gray >= 130):
        return "o"
    elif(gray >= 100):
        return "&"
    elif(gray >= 70):
        return "8"
    elif(gray >= 50):
        return "#"
    else:
        return "@"

def loadGrayScale(im):
    width = im.size[0]
    width = int(width)
    height = im.size[1]
    height = int(height)
    squareArray = [[0 for i in range (height)] for j in range (width)]
    pix = im.load()
    #use disctionary where key is rgb and value is count
    colors = {}
    for i in range (height):
        for x in range(width):
            #where pix[x,i] is the original pixel
            gray = (pix[x,i][0] + pix[x,i][1] + pix[x,i][2]) / 3 
            if(gray in colors):
                colors[gray] = colors[gray] + 1
            else:
                colors[gray] = 0
            #squareArray[x][i] is the grayscale value
            #print(gray)
            squareArray[x][i] = gray
    maxim = (0,0)
    for i in colors:
#        print(colors[i])
        if(colors[i] > maxim[1]):
            maxim = (i,colors[i])
    for i in range (height):
        for x in range(width):
            squareArray[x][i] = detAscii(squareArray[x][i],maxim[0])
    return squareArray

def displayImage():
    for z in range(360):
        clearTerm()

        print("Frame", str(z))
        toOpen = "./Frames/im" + str(z) + ".png"
        im = Image.open(toOpen)
        pix = im.load()
        fin = loadGrayScale(im)
        height = im.size[1]
        height = int(height)
        width = im.size[0]
        width  = int(width)
        im.close()    
        for i in range(height):
            print("")
            for x in range(width):
                print(str(fin[x][i]), end="")
        time.sleep(0.04)

def clearTerm():
    sys.stdout.write("\033c")

@click.command()
@click.argument('videofile')
def main(videofile):
    system("rm -rf ./Frames/im*")
    parseFrames(videofile)
    displayImage()
    system("rm -rf ./Frames/im*")

if __name__ == "__main__":
    main()