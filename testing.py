import lxml
import requests
from lxml import html
import os
import urllib
import csv
import base64
with open('details.csv', 'wb') as file_names:
    writers = csv.writer(file_names)
    writers.writerow(['Title', 'URL'])

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)

# # Example
#
createFolder('./data/')
for page_number in range(24, 102):
    link = "https://www.zoopla.co.uk/for-sale/flats/london/?identifier=london&property_type=flats&page_size=100&q=London&radius=0&pn=" + str(
        page_number)
    response = requests.get(link)
    sourcecode = response.content
    htmlElm = html.document_fromstring(sourcecode)
    print (htmlElm)
    tdElms = htmlElm.cssselect('a.listing-results-address')
    # htmlElm.cssselect()
    # strEle = tdElms[0].text().encode('utf-8')
    # print (strEle)
    i = 0
    array_of_urls = []
    for x in tdElms:
        print(x.get('href'))
        i += 1
        array_of_urls.append(x.get('href'))
    print (i)

    # https://www.zoopla.co.uk/for-sale/details/44936111#tab-floorplan
    values_of_url = 0
    for strings in array_of_urls:
        req = requests.get('https://www.zoopla.co.uk' + strings + '#tab-floorplan')
        image_html = lxml.html.document_fromstring(req.content)
        image_url = image_html.xpath('//*[@id="floorplan-1"]/div[1]/img')
        length_of_url = len(image_url)
        if length_of_url is 0:
            continue
        else:
            str_image_url = image_url[0].get('src')
            print (str_image_url)
            title_url = image_html.xpath('//*[@id="listing-details"]/div[2]/div[1]/h2')
            str_title_url = title_url[0].text_content()
            print (str_title_url)
            correct_string_url = str_title_url
            correct_string_url = correct_string_url.replace('>', ' ')
            correct_string_url = correct_string_url.replace('<', ' ')
            correct_string_url = correct_string_url.replace(':', ' ')
            correct_string_url = correct_string_url.replace('"', ' ')
            correct_string_url = correct_string_url.replace('\\', ' ')
            correct_string_url = correct_string_url.replace('*', ' ')
            correct_string_url = correct_string_url.replace('?', ' ')
            # correct_string_url = correct_string_url.replace('', ' ')

            path_string = './data/' + correct_string_url
            createFolder(path_string)
            title_path_string = './data/' + correct_string_url + '/image.jpg'
            urllib.urlretrieve(str_image_url, title_path_string)
            with open('details.csv', 'a') as f_ile:
                writer = csv.writer(f_ile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([str_title_url, array_of_urls[values_of_url]])
            values_of_url += 1
