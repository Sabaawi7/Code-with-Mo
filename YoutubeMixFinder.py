import webbrowser

video_url = input("Please enter the URL for the requested video: ")


def find_video_id(url):
    video_id_starting_index = url.find("=")
    video_id = url[video_id_starting_index + 1 : video_id_starting_index + 12]
    return video_id


def construct_mix_url(url):
    video_id = find_video_id(url)
    return (
        video_url
        + "&list=RD{video_id}".format(video_id=video_id)
        + "&start_radio=1&rv={}".format(video_id)
    )


try:
    webbrowser.open(construct_mix_url(video_url))

except:
    print("Error")
