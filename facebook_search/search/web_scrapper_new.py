from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
import pandas as pd
from selenium.webdriver import DesiredCapabilities

desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
desired_capabilities['phantomjs.page.customHeaders.User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) ' \
                                                                  'AppleWebKit/537.36 (KHTML, like Gecko) ' \



# br = webdriver.PhantomJS() # it requires phantomjs to be installed in 'usr/local/bin/'
                           # to do it open your terminal and copy and paset this command 'sudo nautilus' and then copy and paste
                           # phantomjs into 'usr/local/bin' folder

br = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs',desired_capabilities=desired_capabilities)
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=1920x1080")

def login(email,pas):
    br.get('https://www.facebook.com')
    # br.get_screenshot_as_file("capture.png")
    file_ = open('chrome.html', 'w')
    file_.write(br.page_source)
    file_.close()
    em = br.find_element_by_name('email')
    em.send_keys(email)
    ps = br.find_element_by_name('pass')
    ps.send_keys(pas)
    print("email pass filled up")
    br.find_element_by_id('loginbutton').click()
    # br.find_element_by_id('loginbutton').click()
    # br.submit()

def save_to_html():
    with open('index.html','r') as f:
        f.writelines(br.page_source)
    print('Data Saved Successfully')

def get_url(url):
    br.get(url)
def scrap():
    source = open('page.html','r')
    sp = BeautifulSoup(source,'html.parser')
    li = sp.find_all('span')
    #f = open('save.txt','w')
    lis = []
    for text in li:
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', str(text))
        lis.append(cleantext)
    print('scarapping complete')
    print("Saving Data on the disk ....")
    fr = pd.DataFrame({'Reviews':lis})
    fr.to_csv('review.csv',columns=fr.columns,index=True)
    print("****Data saved on disk successfully****")

def get_window_elements(wn):
    child_divs = []
    for chld in wn.children:
        child_divs.append(chld)
    return child_divs

def get_post_texts(ls,posts):
    # posts = []
    prof_name = ""
    prof_link = ""
    post_on = ""
    tm = ""
    link = ""
    links = []
    for post in ls:
        res = ""
        prof_name = ""
        prof_link = ""
        post_on = ""
        tm = ""
        link = ""
        para = post.find_all("p")
        # span = post.find_all("span")
        tim = post.find_all("abbr")#timestampContent
        tm = tim[0].attrs["title"]
        lnk = post.find_all("a",{"class":"_5pcq"})
        if len(lnk)>0:
            link = lnk[0].attrs["href"]
        prof = post.find_all("a",{"class":"profileLink"})
        # prof_link = prof[0].attrs["href"]
        if len(prof)>0:
            prof_name = prof[0].text
        post_on_list = post.find_all("a",{"class":"_wpv"})
        if len(post_on_list)!= 0:
            post_on = post_on_list[0].text

        if prof_name== "":
            prof = post.find_all("span",{"class":"fwb fcg"})
            prof_name = prof[0].text
            prof_link = prof[0].find_all("a")[0].attrs["href"]
            post_on_list = post.find_all("a",{"class":"_wpv"})
            if len(post_on_list)!= 0:
                post_on = post_on_list[0].text

        lis = []
        res = ""
        for text in para:
            cleanr = re.compile('<.*?>')
            cleantext = re.sub(cleanr, '', str(text))
            res += " " + cleantext
            # lis.append(cleantext)
        # for text in span:
        #     cleanr = re.compile('<.*?>')
        #     cleantext = re.sub(cleanr, '', str(text))
        #     lis.append(cleantext)
        posts.append((prof_name,prof_link,tm,post_on,res,link))

def output_to_csv(posts):
    author = []
    prof_link = []
    post_time = []
    post_on = []
    status = []
    post_link = []
    facebook = "www.facebook.com"
    for post in posts:
        author.append(post[0])
        if post[1]=="":
            prof_link.append("EMPTY")
        else:
            prof_link.append(post[1])

        post_time.append(post[2])

        if post[3]=="":
            post_on.append("EMPTY")
        else:
            post_on.append(post[3])
        if post[4]=="":
            status.append("EMPTY")
        else:
            status.append(post[4])
        post_link.append(facebook+post[5])

    df = pd.DataFrame({"Author":author,"profile_link":prof_link,"post_time":post_time,"post_on":post_on,"status":status,"post_link":post_link})
    # df.to_excel(name,header=True,index=False,columns=df.columns)
    return df
    print("Saved Sucessfully!")


def Main(key_word):
    email = 'datashall6@gmail.com'
    pas = 'datashallanalytics'
    login(email,pas)
    print('login Successfull')
    # keyword = "banglalink 4g"
    base_url = "https://www.facebook.com/search/str/{}/stories-keyword/".format(key_word.replace(" ","+")) #https://www.facebook.com/search/str/banglalink+4g/stories-keyword/
    br.get(base_url)
    lastHeight = br.execute_script("return document.body.scrollHeight")
    print("Scanning All post .... Please be patience")
    while True:
        br.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(8)
        newHeight = br.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            print("All Review Scanning Done")
            break
        #print("Scanning All Review ....")
        lastHeight = newHeight
    page = br.page_source
    # file_ = open('banglalink.html', 'w')
    # file_.write(page)
    # file_.close()
    # file = open("static/search/banglalink.html","r")
    sp = BeautifulSoup(page,"lxml")
    main_branch = sp.find_all("div",{"class":"_58b7"})
    s = BeautifulSoup(str(main_branch[0]),"lxml")
    divs  = s.div
    ls = []
    for chld in divs.children:
        ls.append(chld)
    ids = []
    for window in ls:
        ids.append(window.attrs["id"])
    posts = []
    for idds in ids[0:-2]:
        window = s.find_all("div",{"id":idds})
        child_divs = get_window_elements(window[0])
        if "fbBrowseScrollingPagerContainer" in idds:
            child_divs = get_window_elements(child_divs[0])
            get_post_texts(child_divs,posts)
        elif "browse_result_below_fold" in idds:
            child_divs = get_window_elements(child_divs[0])
            child_divs = get_window_elements(child_divs[0])
            get_post_texts(child_divs,posts)

        else:
            get_post_texts(child_divs,posts)
    print(len(posts))
    print(len(posts[0]))
    rs = output_to_csv(posts)

    return rs
    # time.sleep(5)
    # url = 'https://m.facebook.com/Grameenphone/photos/a.137318699616926.25404.135237519825044/1970496912965753/?type=3'
    # get_url(url)
    # time.sleep(5)
    # with open("file_posts.html","w") as f:
    #     f.write(br.page_source)
    # h = br.page_source
    # h = BeautifulSoup(h,'html.parser')
    # if 'posts' in url.split("/"):
    #     tx = h.find('div',{'class':'_5rgt _5nk5'}).text
    #     print(tx)
    #     s = h.find('div',{'class':'_52jc _5qc4 _24u0 _36xo'}).a.abbr.string
    #     print(s)
    #     rc = h.find('div',{'class':'_1g06'}).text
    #     rc = list(rc)
    #     if 'K' in rc:
    #         rc = "".join(rc[0:-1])
    #         rc = float(rc)
    #         print("Reactions : {}".format(rc*1000))
    #     else:
    #         rc = float("".join(rc[0:-1]))
    #         print("Reactions : {}".format(rc*1000))
    #     sh = h.find('div',{'class':'_43lx _55wr'}).a.span.text.split(" ")[0]
    #     print("total Shares : {}".format(int(sh)))
    # elif 'photos' in url.split("/"):
    #     tx = h.find('div',{"class":'msg'}).text
    #     print(tx)
    #     tm = int(h.find('div',{'class':'_2vja mfss fcg'}).abbr['data-store'].split(",")[0].split(":")[1])
    #     tm = time.gmtime(tm)
    #     month = ['January','February','March','April','May','June','July','August','September','October','November','December']
    #     s = "Published on "+str(month[tm[1]-1])+" "+str(tm[2])+", "+str(tm[0])
    #     print(s)
    #     rc = h.find('div',{'class':'_1g06'}).text
    #     rc = list(rc)
    #     if 'K' in rc:
    #         rc = "".join(rc[0:-1])
    #         rc = float(rc)
    #         print("Reactions : {}".format(rc*1000))
    #     else:
    #         rc = float("".join(rc[0:-1]))
    #         print("Reactions : {}".format(rc*1000))
    #
    #     sh = h.find('div',{'class':'_43lx _55wr'}).a.span.text.split(" ")[0]
    #     print("total Shares : {}".format(int(sh)))
