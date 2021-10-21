#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import lxml.html
import urllib

membersUrl = "http://www.aph.gov.au/Senators_and_Members/Members/Register"
senatorsUrl = "https://www.aph.gov.au/Parliamentary_Business/Committees/Senate/Senators_Interests/Register46thparl"

def cleanNames(name):
	titles = ['The Hon ','Mr ','Mrs ','Dr ', ' OAM','Ms ', ' AO', ' AM','The  Hon ','the Hon ']
	for title in titles:
		name = name.replace(title,'')
	if "(" in name:
		name = name.split("(")[1].replace(")","")
	nameList = name.split(" ")
	name = nameList[0] + " " + nameList[-1]
	return name.strip().replace(u'\xa0', u' ')   

def getFileName(url):
	if "46p" in url:
		s = url.split("/")[-1].split("?")[0]
		return s
	elif "interests_ctte" in url:
		s = url.split("/")[-1].split("?")[0]
		return s	

r = requests.get(membersUrl)
root = lxml.html.fromstring(r.content)
trs = root.cssselect(".documents tr")

# https://www.aph.gov.au/-/media/03_Senators_and_Members/32_Members/Register/46p/CF/Coleman_46P.pdf?la=en&hash=B5AC0DDEEA0173AFD9A94DC43D1DF0DE533AABB5
# https://www.aph.gov.au/-/media/Committees/Senate/committee/interests_ctte/Statements_2019_46th_Parl/AbetzE_Astat_190726.pdf?la=en&hash=9CC9066DA52EE708F580261A5323122945E57A35

for tr in trs:
		tds = tr.cssselect("td")
		if tds:
			dateUpdated = tds[0].text

			blahStr = lxml.html.tostring(tds[2], encoding = "unicode")
			if "<a" in blahStr:
				print(tds[2].cssselect("a")[0].attrib['href'])
				interestsUrl = "http://www.aph.gov.au/" + tds[2].cssselect("a")[0].attrib['href']
				print(interestsUrl)
				politicianName = tds[1].text.split(",")[1].strip() + " " + tds[1].text.split(",")[0].strip()
				politicianName = cleanNames(politicianName)
				fileName = getFileName(interestsUrl)
				r2 = requests.get(interestsUrl)
				with open(f'pdfs/{fileName}', 'wb') as f:
					f.write(r2.content)
#%%
r = requests.get(senatorsUrl)
root = lxml.html.fromstring(r.content)
trs = root.cssselect(".columns tr")

# https://www.aph.gov.au/-/media/03_Senators_and_Members/32_Members/Register/46p/CF/Coleman_46P.pdf?la=en&hash=B5AC0DDEEA0173AFD9A94DC43D1DF0DE533AABB5
# https://www.aph.gov.au/-/media/Committees/Senate/committee/interests_ctte/Statements_2019_46th_Parl/AbetzE_Astat_190726.pdf?la=en&hash=9CC9066DA52EE708F580261A5323122945E57A35

for tr in trs:
		tds = tr.cssselect("td")
		if tds:
# 			dateUpdated = tds[0].text

			blahStr = lxml.html.tostring(tds[0], encoding = "unicode")
			if "<a" in blahStr:
				print(tds[0].cssselect("a")[0].attrib['href'])
				interestsUrl = "http://www.aph.gov.au/" + tds[0].cssselect("a")[0].attrib['href']
				print(interestsUrl)
				politicianName = tds[0].cssselect("a")[0].text.split(",")[1].strip() + " " + tds[0].cssselect("a")[0].text.split(",")[0].strip()
				politicianName = cleanNames(politicianName)
				fileName = getFileName(interestsUrl)
				r2 = requests.get(interestsUrl)
				with open(f'pdfs/{fileName}', 'wb') as f:
					f.write(r2.content)					
					