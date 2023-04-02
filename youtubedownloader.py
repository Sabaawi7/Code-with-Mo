from pytube import YouTube

# URL of the YouTube video
url = input("Please type in the requested URL: ")

# Resolution
res = input("Please type in in which resolution it should be downloaded: ")

# Create a YouTube object
yt = YouTube(url)

# Get the video with the highest resolution
video = yt.streams.get_by_resolution(res)

# Save the video to the current directory
video.download("../../Downloads", str(yt.title + ".mp4"))

print("Download Successfull")
