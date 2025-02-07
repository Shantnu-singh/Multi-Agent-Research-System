from youtube_transcript_api import YouTubeTranscriptApi , NoTranscriptFound

def GetTranscripts(youtube_link):
  if youtube_link:
    youtube_code = youtube_link.split("v=")[1]
    try :
        out = YouTubeTranscriptApi.get_transcript(youtube_code)
    except NoTranscriptFound:
        transcript_list = YouTubeTranscriptApi.list_transcripts(youtube_code)
        for transcript in transcript_list:
            out = transcript.translate('en').fetch()
            # print(out)
            # return
    except :
        return "Can't return anything as the video might not exist"
            
    main_text = ""
    for lst in out:
        if lst['text'] != "[MUSIC]":
            main_text += lst['text'] + " "
    
    return main_text

print(GetTranscripts("https://www.youtube.com/watch?v=RuwFDrljlmY"))