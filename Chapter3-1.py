import requests

url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=it&dt=t&q=hello"
url2 = "https://translate.googleapis.com/translate_a/single?client=gtx&sl={}&tl={}&dt=t&q={}".format('en','it','hello')
r = requests.get(url2)
r.raise_for_status
print(r.json())
