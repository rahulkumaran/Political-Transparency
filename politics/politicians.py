from bs4 import BeautifulSoup
import requests
import pytesseract
from PIL import Image
from io import BytesIO
import os
import pandas as pd

class PoliticiansData:
    def __init__(self, state):
        self.state = state

    def get_state_politicians_profiles(self):
        url = "https://nocorruption.in/state/" + self.state
        r=requests.get(url)
        soup=BeautifulSoup(r.content,'html.parser')
        table_box = soup.find(class_='span12')
        links = table_box.find_all('a', href=True)
        f = open(self.state + "_links.txt","w+")
        politician_names = []
        politician_links = []
        for a in links:
            politician_names += [a.text]
            politician_links += [a.get('href')]
            f.write(a.get('href')+'\n')
        f.close()

        f = open(self.state + "_links.txt","r")
        links = open(self.state + "_politicians_profiles.txt","w+")
        for line in f:
            if("politician" not in line):
                continue
            else:
                links.write(line)
        f.close()
        links.close()
        os.remove(self.state + "_links.txt")

        return 1

    def get_state_politicians_data(self):
        status = self.get_state_politicians_profiles()
        links = open(self.state + "_politicians_profiles.txt","r")
        details = open(self.state + "-Politicians.csv","w+")
        for line in links:
            try:
                url = line.replace('\n',"")
                r = requests.get(url)
                img_link = ""
                soup = BeautifulSoup(r.content,'html.parser')
                name = soup.find(class_='jumbotron subhead')
                emails = soup.find_all('img')
                for email in emails:
                    if("email.php?" in str(email)):
                        img_link = email['src']
                        break
                r = requests.get(img_link)
                num = soup.find_all(class_='table table-striped table-bordered')
                email = pytesseract.image_to_string(Image.open(BytesIO(r.content)))
                email = email.replace(" ","")
                if("con" in email):
                    email = email.replace("con","com")
                    email = email.replace("gnail","gmail")
                    email = email.replace("rediffnail", "rediffmail")
                try:
                    details.write(name.text + "," + num[1].text.split("Number")[1][0:10] + "," + email)
                except:
                    details.write(name.text + ",NA" + "," + email)
            except:
                continue

        links.close()
        details.close()
        os.remove(self.state + "_politicians_profiles.txt")

        return pd.read_csv(self.state + "-Politicians.csv")

if(__name__=='__main__'):
    p = PoliticiansData("Karnataka")
    data = p.get_state_politicians_data()

    print(data.head())
