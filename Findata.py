import requests, beautifulsoup4


r = requests.get("https://example.com/")

r.status_code
print(r.text)


file = open("test_text1.txt", "w") 
file.write(r.text)
file.close()