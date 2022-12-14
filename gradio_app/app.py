from gradio import Interface,Textbox,Series
from requests import get
from re import sub

def clean_text(text):
    """it cleans subtitle text of ted talks

    Args:
        text (str): subtitle of ted talk

    Returns:
        cleaned_text (str): cleaned version of subtitle text 
    """
    #remove string inside parantheses (i.e appluse)
    text=sub(r'\(.*\)', '', text)
    #format text by splitting/removing new lines
    text=text.split("\n")[1:]
    #remove empty strings
    text=list(filter(None, text))
    #remove timestamps as they contains pattern of "-->"
    cleaned_text=" ".join([x.strip() for x in text if "-->" not in x])
    return cleaned_text

def ted_talk_transcriber(link):
    """it yields transcription of ted talks from url

    Args:
        link (str): url link of ted talks

    Returns:
        cleaned_transcript (str): transcription of the ted talk
    """
    #request link of the talk
    page = get(link)
    #extract unique talk id to reach subtitle file
    talk_id=str(page.content).split("project_masters/")[1].split("/")[0]
    raw_text = get(f'https://hls.ted.com/project_masters/{talk_id}/subtitles/en/full.vtt').text
    cleaned_transcript=clean_text(raw_text)
    return cleaned_transcript

transcriber = Interface(ted_talk_transcriber,
                        'text',
                        'text',
                        )

summarizer = Interface.load("huggingface/pszemraj/long-t5-tglobal-base-16384-book-summary")

logo = f"<center><img src='file/TED.png' width=180px></center>"

Series(transcriber,
        summarizer,
        inputs = Textbox(label = "Type the TED Talks link"),
        examples = ["https://www.ted.com/talks/jen_gunter_the_truth_about_yeast_in_your_body"],
        allow_flagging="never",
        description = logo,
        ).launch()