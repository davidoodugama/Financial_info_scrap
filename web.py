from bs4 import BeautifulSoup
import requests
import time

print("Put some skills that you are not familiar with")
unfamiliar_skill = input('>')
print(f"Filtering out {unfamiliar_skill}")

def find_jobs():
    html_test = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=python&txtLocation=').text
    soup = BeautifulSoup(html_test, 'lxml')

    jobs = soup.find_all('li', class_= 'clearfix job-bx wht-shd-bx')

    for job in jobs:
        published_date = job.find('span', class_= 'sim-posted').span.text
        if 'few' in published_date:
            company_name = job.find('h3', class_='joblist-comp-name').text.replace(' ','')
            skills = job.find('span', class_= 'srp-skills').text.replace(' ','')
            # just for knowledge
            # To check if a specific name is in a tag or not
            # tags = job.find_all(["option"], text = "Undergrads") # in here option is the tag name and the text we are going to find is undergrads
            
            if unfamiliar_skill not in skills:
                more_info = job.header.h2.a['href']
                print(f"Company Name: {company_name.strip()}")
                print(f"Skills: {skills.strip()}")
                print(f'More info: {more_info}')
                print('')

if __name__ == "__main__":
    while True:
        find_jobs()
        time_wait = 10
        print(f"Wating {time_wait * 60} seconds")
        time.sleep(time_wait * 60)
        