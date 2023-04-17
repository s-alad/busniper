import requests

cookies = {
    'JSESSIONID': 'nmsgul53vrpepvnymo5s0nue',
    'apt.uid': 'AP-PQQY5YJEHTTA-2-1674153969834-32452642.0.2.da0f3d99-a9c8-4b0c-b212-9618d031552a',
    'AWSALB': '+CdT2YEC160NAsVe8ilduBR5NVyn6HXOaRBr9wNin/il8ah5VnFGdmiMfaq7I6gzjuaqEgmtk6Be0fyEnrYPcn0cCayDCWadsascCBEHlU9hQkuk1zXT8x0uvnE5',
    'AWSALBCORS': '+CdT2YEC160NAsVe8ilduBR5NVyn6HXOaRBr9wNin/il8ah5VnFGdmiMfaq7I6gzjuaqEgmtk6Be0fyEnrYPcn0cCayDCWadsascCBEHlU9hQkuk1zXT8x0uvnE5',
    'BIGipServershib-ist-idp-prod-443-pool': '1927726464.47873.0000',
    'uiscgi_prod': '518130c8457ef74a6c7f44d8c92b6b52:prod',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://shib.bu.edu/idp/profile/SAML2/POST-SimpleSign/SSO;jsessionid=nmsgul53vrpepvnymo5s0nue?execution=e1s1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://shib.bu.edu',
    'DNT': '1',
    'Connection': 'keep-alive',
    # 'Cookie': 'JSESSIONID=nmsgul53vrpepvnymo5s0nue; apt.uid=AP-PQQY5YJEHTTA-2-1674153969834-32452642.0.2.da0f3d99-a9c8-4b0c-b212-9618d031552a; AWSALB=+CdT2YEC160NAsVe8ilduBR5NVyn6HXOaRBr9wNin/il8ah5VnFGdmiMfaq7I6gzjuaqEgmtk6Be0fyEnrYPcn0cCayDCWadsascCBEHlU9hQkuk1zXT8x0uvnE5; AWSALBCORS=+CdT2YEC160NAsVe8ilduBR5NVyn6HXOaRBr9wNin/il8ah5VnFGdmiMfaq7I6gzjuaqEgmtk6Be0fyEnrYPcn0cCayDCWadsascCBEHlU9hQkuk1zXT8x0uvnE5; BIGipServershib-ist-idp-prod-443-pool=1927726464.47873.0000; uiscgi_prod=518130c8457ef74a6c7f44d8c92b6b52:prod',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Sec-GPC': '1',
}

params = {
    'execution': 'e1s1',
}

data = {
    'j_username': '',
    'j_password': '',
    '_eventId_proceed': '',
}

response = requests.post(
    'https://shib.bu.edu/idp/profile/SAML2/POST-SimpleSign/SSO',
    params=params,
    cookies=cookies,
    headers=headers,
    data=data,
)

print(response.text)