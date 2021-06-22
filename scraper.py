from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import csv

starturl = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome("C:/Users/abhin/Downloads/chromedriver_win32 (1)/chromedriver")
browser.get(starturl)
time.sleep(10)
planetData = []
newplanetdata = []

def scrape():
    headers = ["Name", "LightyearsFromEarth",  "PlanetMass", "StellarMagnitude", "DiscoveryDate", "HyperLink", "planet_type", "planet_radius", "oribital_radius", "orbital_period", "eccentrcity"]
    for i in range(0, 10):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        for l in soup.find_all("ul", attrs = {"class", "exoplanet"}):
            litags = l.find_all("li")
            tempList = []
            for index, litag in enumerate(litags):
                if index == 0:
                    tempList.append(litag.find_all("a")[0].contents[0])
                else:
                    try:
                        tempList.append(litag.contents[0])
                    except:
                        tempList.append("")
            hyperlink_li_tag = litags[0]
            tempList.append("https://exoplanets.nasa.gov/" + hyperlink_li_tag.find_all("a", href = True)[0]["href"])
            planetData.append(tempList)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

def scrapemoredata(hyperlink_li_tag):
    page = requests.get(hyperlink_li_tag)
    soup = BeautifulSoup(page.content, "html.parser")
    for tr_tag in soup.find_all("tr", attrs = {"class": "fact_row"}):
        td_tags = tr_tag.find_all("td")
        temp_list = []
        for td_tag in td_tags:
            try:
                temp_list.append(td_tag.find_all("div", attrs = {"class":"value"})[0].contents[0])
            except:
                temp_list.append("")
        newplanetdata.append(temp_list)

scrape()

for index, data in enumerate(planetData):
    scrapemoredata(data[5])

finalPlanet = []

for index, data in enumerate(planetData):
    newplanetelement = newplanetdata[index]
    newplanetelement = [elem.replace("\n", "")for elem in newplanetelement]
    newplanetelement = newplanetelement[:7]
    finalPlanet.append(data + newplanetelement)

with open("Planets1.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(finalPlanet)