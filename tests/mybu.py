import requests

#bmsv changes
cookies = {
    'renderCtx': '%7B%22pageId%22%3A%220aee1679-030e-468a-a825-2852a6f402a9%22%2C%22schema%22%3A%22Published%22%2C%22viewType%22%3A%22Published%22%2C%22brandingSetId%22%3A%225c292461-29b3-49ed-894d-e1cc1ef88a23%22%2C%22audienceIds%22%3A%226Au3o000000fxaK%2C6Au0V000000XZIG%2C6Au3o000000fxZb%2C6Au3o000000fxaP%2C6Au3o000000XZO9%2C6Au3o000000fxbr%2C6Au0V000000XZIQ%2C6Au3o000000fxaZ%2C6Au460000004FIo%2C6Au3o000000fxaa%2C6Au3o000000Gmhe%2C6Au460000004Gdq%2C6Au3o000000fxae%2C6Au3o000000fxao%2C6Au460000004GmF%2C6Au3o000000XZOY%2C6Au0V000000PB5W%2C6Au3o000000GmhZ%2C6Au0V000000XZI1%2C6Au460000004FJI%2C6Au3o000000fxbX%2C6Au3o000000Gmi8%2C6Au0V000000XZHw%2C6Au460000004Gi0%2C6Au3o000000fxbh%22%7D',
    'sid': '00D46000000pQ8F!ARkAQP_6LE7SWhSkSV5phcdoYicTFbBRJPcn0fGot2SBsKBZ1f230uAMMfLBftC3iqaYEkE3gohnM.cFxgIeXQOWX5z22lNN',
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
    # 'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Sec-GPC': '1',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

response = requests.get('https://bu.my.site.com/myBU/s/', cookies=cookies, headers=headers)
print(response)