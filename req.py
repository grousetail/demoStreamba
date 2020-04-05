import requests
import urllib.parse
posturl="https://www.reddit.com/r/pics/comments/fubdg0/when_the_light_hits_just_right/"

r = requests.post("http://127.0.0.1:5000/", data={'url': posturl})
print(r.text) 