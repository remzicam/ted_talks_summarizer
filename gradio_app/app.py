"""TED Talks Summarizer App."""

from re import sub

from gradio import Interface, Textbox
from requests import get
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

repo_id = "pszemraj/led-base-book-summary"

model = AutoModelForSeq2SeqLM.from_pretrained(
    repo_id,
    low_cpu_mem_usage=True,
)

tokenizer = AutoTokenizer.from_pretrained(repo_id)

summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)


def clean_text(text: str) -> str:
    """Cleans subtitle text of ted talks.

    Args:
        text (str): subtitle of ted talk

    Returns:
        cleaned_text (str): cleaned version of subtitle text
    """
    # remove string inside parantheses (i.e appluse)
    text = sub(r"\(.*\)", "", text)
    # format text by splitting/removing new lines
    text = text.split("\n")[1:]
    # remove empty strings
    text = list(filter(None, text))
    # remove timestamps as they contains pattern of "-->"
    cleaned_text = " ".join([x.strip() for x in text if "-->" not in x])
    return cleaned_text


def ted_talk_transcriber(link: str) -> str:
    """Creates transcription of ted talks from url.

    Args:
        link (str): url link of ted talks

    Returns:
        raw_text (str): raw transcription of the ted talk
    """
    # request link of the talk
    page = get(link)
    # extract unique talk id to reach subtitle file
    talk_id = str(page.content).split("project_masters/")[1].split("/")[0]
    raw_text = get(
        f"https://hls.ted.com/project_masters/{talk_id}/subtitles/en/full.vtt"
    ).text
    return raw_text


def text_summarizer(text: str) -> str:
    """Summarizes given text.

    Args:
        text (str): ted talks transcription

    Returns:
        str: summary
    """
    result = summarizer(
        text,
        min_length=8,
        max_length=256,
        no_repeat_ngram_size=3,
        encoder_no_repeat_ngram_size=3,
        repetition_penalty=3.5,
        num_beams=4,
        do_sample=False,
        early_stopping=True,
    )
    return result[0]["summary_text"]


def main(link: str) -> str:
    """Summarizes ted talks given link.

    Args:
        link (str): url link of ted talks

    Returns:
        str: summary
    """
    raw_text = ted_talk_transcriber(link)
    cleaned_transcript = clean_text(raw_text)
    return text_summarizer(cleaned_transcript)


logo = "<center><img src='file/TED.png' width=180px></center>"

Interface(
    main,
    inputs=Textbox(label="Type the TED Talks link"),
    examples=[
    "https://www.ted.com/talks/jen_gunter_the_truth_about_yeast_in_your_body"
             ],
    outputs=Textbox(label="Summary"),
    allow_flagging="never",
    description=logo,
).launch()
