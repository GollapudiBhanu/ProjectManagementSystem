def readmoreDriverElement(self, url, link_text):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--blink-settings=imagesEnabled=false')
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        driver.get(url)
    except:
        pass
    try:
        driver.find_element_by_link_text('Read more').click()
        data = wait.until(EC.presence_of_element_located((By.ID, 'overview-text')))
        print(data.text)

    except:
        print('error')

    def getSinglePageReviews(self, project_soup):
        data = {}
        section = project_soup.findAll('div', attrs={'class': 'review-copy-container'})
        try:
            profile_name = section[0].findAll('p', attrs={'class': 'ui'})[0].text
            data['User_Name'] = profile_name
        except:
            data['User_Name'] = None
        try:
            header = section[0].findAll('p', attrs={'class': 'review-copy-header strong'})[0].text
            data['Review_Title'] = header
        except:
            data['Review_Title'] = None

        try:
            s = section[0].find_all("p", {"class": "ui"})
            try:
                data['Review_Description'] = s[0].text
            except:
                data['Review_Description'] = None
            try:
                data[s[1].text] = s[2].text
            except:
                data['Pros'] = None
            try:
                data[s[3].text] = s[4].text
            except:
                data['Cons'] = None
            try:
                data[s[5].text] = s[6].text
            except:
                data['Reasons for switching to Workzone'] = None
        except:
            data['Review_Description'] = None
            data['Pros'] = None
            data['Cons'] = None
            data['Reasons for switching to Workzone'] = None

        print('#################')
        return [data]

    def getReviews(self, url):
        review_pages_list = []
        for i in range(1, 12):
            request_url = url + '?review.page=' + str(i)
            self.driver.get(request_url)
            html = self.driver.page_source
            project_soup = BeautifulSoup(html, 'html.parser')
            try:
                right_button = project_soup.find('div', class_="pagination-arrows-right")
                reviews_list = project_soup.findAll('div', attrs={'class': 'reviews'})
                review_pages_list.append(reviews_list[0])
                if right_button is None:
                    break
            except:
                continue
        data_list = self.getPaginationReviews(review_pages_list)
        return data_list

    def getPaginationReviews(self, review_pages_list):
        data_list = []
        for review_page in review_pages_list:
            for div in review_page[0].findAll('div', attrs={'class': 'review'}):
                data = {}
                try:
                    profile_name = div.findAll('p', attrs={'class': 'ui'})[0].text
                    data['User_Name'] = profile_name
                except:
                    data['User_Name'] = None

                try:
                    header = div.findAll('p', attrs={'class': 'review-copy-header strong'})[0].text
                    data['Review_Title'] = header
                except:
                    data['Review_Title'] = None

                try:
                    review_summary = div.findAll('div', attrs={'class': 'review-copy-container'})
                    s = review_summary[0].find_all("p", {"class": "ui"})
                    try:
                        data['Review_Description'] = s[0].text
                    except:
                        data['Review_Description'] = None
                    try:
                        data[s[1].text] = s[2].text
                    except:
                        data['Pros'] = None
                    try:
                        data[s[3].text] = s[4].text
                    except:
                        data['Cons'] = None
                    try:
                        data[s[5].text] = s[6].text
                    except:
                        data['Reasons for switching to Workzone'] = None
                except:
                    data['Review_Description'] = None
                    data['Pros'] = None
                    data['Cons'] = None
                    data['Reasons for switching to Workzone'] = None

                data_list.append(data)

            return data_list

        try:
            review_summary = div.findAll('div', attrs={'class': 'review-copy-container'})
            s = review_summary[0].find_all("p", {"class": "ui"})
            try:
                data['Review_Description'] = s[0].text
            except:
                data['Review_Description'] = None
            try:
                data[s[1].text] = s[2].text
            except:
                data['Pros'] = None
            try:
                data[s[3].text] = s[4].text
            except:
                data['Cons'] = None
            try:
                data[s[5].text] = s[6].text
            except:
                data['Reasons for switching to Workzone'] = None
        except:
            data['Review_Description'] = None
            data['Pros'] = None
            data['Cons'] = None
            data['Reasons for switching to Workzone'] = None



        #single review

        if i == 0:
            data['Review_Title'] = div.text
        elif i == 2:
            data['Pros'] = div.text
        elif i == 4:
            data['Cons'] = div.text


    def getReviewLink(self, url):
        page = urlopen(url)
        html = page.read().decode("utf-8")
        project_soup = BeautifulSoup(html, 'html.parser')
        section = project_soup.findAll('div', attrs={'class': 'MenuItemComponent column menu__item'})
        link = section[0].find('a').get('href')
        if link is None:
            self.getSinglePageReviews(project_soup)
        else:
            return link
