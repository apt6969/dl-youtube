This was created to get criminal evidence for specifically xqc on YouTube, but I guess you could use it for whatever you want. This actually loads the videos including sound in a headless browser so you may want to mute your computer when running it.

Usage python3 (or python) dl_youtube.py term1 term2 term3 etc.

Optional Arguments: -NV (flag for "no videos", which will skip the video downloading part for you)

---

Sample usage in head mode so you could see what's going on: https://www.youtube.com/watch?v=decXxjg0lAY

I included a chromedriver executable (mac arm64 114.0.5735.90) but you basically just need to install whatever version matches your Chrome browser (separately installed) and OS. https://chromedriver.chromium.org/downloads

---

Example usage: python3 dl_youtube.py xqc gambling

Example usage 2: python3 dl_youtube.py xqc criminal -NV

Example usage 3: python3 dl_youtube.py twitch crimes

Example usage 4: python3 dl_youtube.py twitch 

---

Right now it traverses 20 links from any YouTube query, stores the urls in a csv, gets full page screenshots, and downloads videos if you want. Just add and adjust anything to fit your purpose...

---

I am in support and appreciation for President Biden's stance. However, why not take lawful things into your own hands? There's no "online tresspassing" laws so you could just spook the living daylights out of the criminals on the Internet....

![Image 6-21-23 at 8 02 PM](https://github.com/bshang165/dl-youtube/assets/118570793/569b418a-e7bd-4ed8-8f47-41323b8277bf)
