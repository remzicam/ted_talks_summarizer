# Ted Talks Summarizer
<center><img src="gradio_app/TED.png" width=250px></center>

This project aims to summarize TED talks (https://www.ted.com/) videos. It creates short summary of ted talk from given url.


App demo link:

https://huggingface.co/spaces/remzicam/ted_talks_summarizer

The process can be slow in huggingface space. Alternatively you can try it on google colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/remzicam/ted_talks_summarizer/blob/main/ted_talk_summarizer.ipynb)

Sample from app:

<img src="app_ss.png">

# Business Problem

&bull; By providing summaries of these talks, your app allows people to quickly and easily get the main points and key ideas from a talk without having to watch the entire video. This can be particularly useful for busy professionals who want to stay up-to-date with the latest ideas and trends in their field.
&bull; It could also be useful for students or educators who want to use TED Talks as a learning resource, but need a way to quickly understand the key points of a talk in order to integrate it into their coursework or lectures.

# Tools Used:

&bull; gradio (web app)
&bull; transformers (summarizer model)
&bull; requests (to get the subtitle link)
&bull; regex (to clean text)
&bull; huggingface spaces (to host my app)
