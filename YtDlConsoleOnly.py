from pytube import YouTube

while True:
    link = input("Enter the Youtube Link: ")
    yt = YouTube(link)
    dlformat = input("Choose Format (1: MP3 ; 2: MP4): ")
    

    if dlformat == '1' or dlformat == '2':
        print("Currently Downloading: " + yt.title)
    else:
        print ("Please enter either 1 or 2 only.")
        dlformat = input("Choose Format (1: MP3 ; 2: MP4): ")
            
    if dlformat == "1":
        stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        stream.download(output_path='.', filename_prefix='audio-')
        fileFormat = "MP3"
        
    elif dlformat == "2":
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        stream.download()
        fileFormat = "MP4"
    
    
    print("Successfully downloaded the youtube video in {} format".format(fileFormat))
    exit1 = input("Do you want to continue? (1: Continue Downloading , 2: Exit): ")
    
    if exit1 == '1':
        continue
    else:
        break
    
    
# https://www.youtube.com/watch?v=dQw4w9WgXcQ

#This program displays some of the language's programming theories
    # Type Binding
    # Control Constructs
    # Variable Declarations 
    # Syntax
    # Libraries