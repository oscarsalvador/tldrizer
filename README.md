# TLDRizer
A simple python app that uses yt-dlp to download audio, OpenAI Whisper to transcribe it, and Mistral 7b with Langchain to generate a summary of transcriptions of any length. 

To run, clone the repo and run the `start.sh` script. Because the proyect is built with nvidia docker containers, you don't need to worry about libraries in your system. The GUI is displayed by sharing the X11 unix socket with the container, making it possible for apps to show display their interfaces on the host's session.


![](/output.gif)
