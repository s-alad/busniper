import requests

cookies = {
    'sid': '00D46000000pQ8F^!ARkAQP_6LE7SWhSkSV5phcdoYicTFbBRJPcn0fGot2SBsKBZ1f230uAMMfLBftC3iqaYEkE3gohnM.cFxgIeXQOWX5z22lNN',
    'sid_Client': 'o000008FllL6000000pQ8F',
    'clientSrc': '128.197.29.242',
    'inst': 'APP_3o',
    'CookieConsentPolicy': '0:1',
    'LSKey-c$CookieConsentPolicy': '0:1',
    'BrowserId': 'EUfCV9yQEe23Gy8jnQ94JA',
    'BrowserId_sec': 'EUfCV9yQEe23Gy8jnQ94JA',
    'ak_bmsc': 'EF6057DD3FF3C461776AA216D47CA916~000000000000000000000000000000~YAAQraomF1CPaXKHAQAAMUifixMEAQ91u82/0KpP8Tp8gIVaZKDEGJ4A2h+XJj3tNxbbjuguwmlleGycc3gjp6lgz6rU3tOXLbP4JyORJ/ifgqy0ed/96A2VLevVYkIw08TSrOl6FwN/APvT4C65V0j+Ivc3AtSujQI3sJSztFEkSQs/ULL4jdQQU9kxXUxOk/4EnbACIMmrLzDTNbb5UlWWKRzdJnlWnVwCmc6HKm5QLZzhRLlXhniok74XbuEqlzluQTM5Z7R9Cn0zD3oSkycg21LXiXeexkNfMYLSZgikily8okDjJ5IInT1RRSAxMCvtWu0cWY+31OAdVe47w4s2AknN2Tw8OcxjM0b/51BomyFZRy1/YdDrfQjiJjQvuJesBOlWkAJfmifp',
    'bm_sv': '8FFC8B4F387FA7F52BD2FB68340B623C~YAAQTr4cuNxnEXKHAQAA6xCnixN7f6FXJEoXOejg03us4pg4vY1kKLjibYc6y55yPbwykrYzB850/BC/GGqBEn9MwEpi/aGCdxpPKUbR8NIKjqysNAOsvJuxRYOKniCvjdSkyuw6laqjh+AmbKE3nY15i66m9U3WAd1QqakztZ+n8gZLDxXnkUXNSmpO6K1spjwTt4/Z06+LNofJSgXnfves2lXeHg661hNvFHbuJcrBu0l8fG4gL9871vjF8n/YGPo=~1',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Sec-GPC': '1',
}

response = requests.get('https://bu.my.site.com/myBU/', cookies=cookies, headers=headers)
#print response cookies
print(response.cookies)