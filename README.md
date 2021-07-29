<div align="center">

<img src="https://user-images.githubusercontent.com/17500203/126075885-0da5d897-9af6-4fad-b0f7-ac40635ee6c1.png" width=300>

# Jesture AI SDK

<!-- [![JestureAiSdkReadmeHeaderGithub](https://user-images.githubusercontent.com/17500203/124357142-a6c72580-dc22-11eb-8838-b59ca69ef1f6.png)](https://github.com/jesture-ai/jesture-sdk) -->

**Real-time gesture control made accessible.**

[![YouTube](https://img.shields.io/badge/videos-youtube-white)](https://www.youtube.com/watch?v=sxaZ_yLgtLk&list=PL4Z9jysfxyfj9F1Kfdy_4oXKX9-MESCpP&index=1)
[![Twitter](https://img.shields.io/badge/news-twitter-1DA1F2)](https://twitter.com/jestureai)
[![Website](https://img.shields.io/badge/official-website-3fbeeb)](https://www.jesture.ai)
[![Instagram](https://img.shields.io/badge/follow-instagram-bc2a8d)](https://www.instagram.com/jesture.ai)
  
</div>

---

## Use-cases with Jesture AI SDK
Immersive Gaming | Web Apps                                                                                          
:----------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------: 
![gaming](docs/gifs/afterspell.gif)| ![web](docs/gifs/web.gif)

Slides Control | Visual Effects                                                                                                         
:-------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------:
![slides](docs/gifs/slides.gif)| ![snap](docs/gifs/viz.gif)

Music Control | Snap Masks                                                                                                                     
:-------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------:
![slides](docs/gifs/itunes.gif)| ![snap](docs/gifs/snap-zoom.gif)

## Install

### MacOS

1. Clone this repo: `git clone https://github.com/jesture-ai/jesture-sdk`
2. Download the latest version of SDK from the [Releases](https://github.com/jesture-ai/jesture-sdk/releases) page
3. Place the downloaded archive into the `jesture_sdk/` folder and unzip it there:
```
jesture_sdk/
|-- install.sh
|-- remove.sh
|-- full_cpu.dylib
|-- third_party/
|-- mediapipe/
|-- third_party/
```
5. Install the dependencies: `sudo bash install.sh`
6. You are all set! Checkout the [Python demo](https://github.com/jesture-ai/jesture-sdk/tree/main/python) to learn how to run the SDK in Python.

If one wish to remove all the dependencies: `sudo bash remove.sh`.

**Note:** The script `install.sh` just copies the dependencies to `/usr/local/Cellar/jestureai/` and `/usr/local/opt/jestureai/` paths. To access them it requires priviledged access (`sudo`).

### Windows

SDK is not yet available on Windows. Stay tuned!

### Attribution 

See the `LICENSE` for more details on 3rd party software. 

<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
