from threading import Thread
from yt_dlp import YoutubeDL
from langchain.chains import MapReduceDocumentsChain, LLMChain, ReduceDocumentsChain, StuffDocumentsChain
from langchain.llms import CTransformers
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.document_loaders import (TextLoader)
from langchain.docstore.document import Document
from ctransformers import AutoModelForCausalLM
import whisper
import tkinter as tk
import os
import subprocess
import time
import json



def download(gui):
  print("\ndownload")
  gui.video_path = "/tmp/" + str(int(time.time()))

  options = {
    "format": "bestaudio",
    "outtmpl": gui.video_path ,
    'postprocessors': [{
      'key': 'FFmpegExtractAudio',
      'preferredcodec': 'm4a',
    }],
  }

  try:
    with YoutubeDL(options) as ytdl:
      info = ytdl.extract_info(gui.url.get(), download=False)
      gui.title.config(text=info.get("title", None))
      gui.video_len.config(text= time.strftime("%H:%M:%S", time.gmtime(info.get("duration", None))))
      gui.update_progressbar(1)


      result = ytdl.download([gui.url.get()])
      gui.update_progressbar(2)
      return True
  except Exception as e:
    print("Error in download: ", e)
    gui.clear()
    gui.title.config(text="Error, bad URL")
    return False




def transcribe(gui):
  print("\ntranscribe")

  model = whisper.load_model("base", download_root=gui.models_dir, device="cuda")
  gui.update_progressbar(2)

  # model = whisper.load_model("base", device="cuda")
  transcript = model.transcribe(gui.video_path + ".m4a")
  gui.update_progressbar(4)

  gui.capt_text = transcript["text"]
  gui.capt_segments = transcript["segments"]
  gui.fill_l_text()


def summarize(gui):
  print("\nsummarize")
  # loader = TextLoader(gui.capt_text)
  # docs = loader.load()
  docs = [Document(page_content=gui.capt_text)]

  config = {'max_new_tokens': 4096, 'temperature': 0.7, 'context_length': 4096, 'gpu_layers': 50}
  
  llm = CTransformers(model="TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
    model_file="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    config=config,
    threads=os.cpu_count(),
    device=0
  )

  gui.update_progressbar(4)

  map_template = """<s>[INST] The following is a part of a transcript:
  {docs}
  Based on this, please identify the main points.
  Answer:  [/INST] </s>"""
  map_prompt = PromptTemplate.from_template(map_template)
  map_chain = LLMChain(llm=llm, prompt=map_prompt)

  reduce_template = """<s>[INST] The following is set of summaries from the transcript:
  {doc_summaries}
  Take these and distill it into a final, consolidated summary of the main points.
  Construct it as a well organized summary of the main points and should be between 3 and 5 paragraphs.
  Answer:  [/INST] </s>"""
  reduce_prompt = PromptTemplate.from_template(reduce_template)
  reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

  combine_documents_chain = StuffDocumentsChain(
    llm_chain=reduce_chain, document_variable_name="doc_summaries"
  )

  reduce_documents_chain = ReduceDocumentsChain(
    combine_documents_chain=combine_documents_chain,
    collapse_documents_chain=combine_documents_chain,
    token_max=4000,
  )

  map_reduce_chain = MapReduceDocumentsChain(
    llm_chain=map_chain,
    reduce_documents_chain=reduce_documents_chain,
    document_variable_name="docs",
    return_intermediate_steps=True,
  )


  text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=4000, chunk_overlap=0
  )
  split_docs = text_splitter.split_documents(docs)

  gui.update_progressbar(2)

  start_time = time.time()
  result = map_reduce_chain.__call__(split_docs, return_only_outputs=True)
  gui.update_progressbar(8)

  print(f"Time taken: {time.time() - start_time} seconds")

  gui.summ_text = result['output_text']
  gui.fill_r_text()