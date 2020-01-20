from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import sys

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def get_splits(l):
  rh = simple_get(l)
  h = BeautifulSoup(rh, 'html.parser')
  t = ""
  # name
  n = h.find("h4").string
  t = t + n + ", "

  # bib and gender
  tables = h.find_all("table")
  pd = tables[1]
  pdrtable = pd.find("table")
  bib = pdrtable.find_all("tr")[2].find_all("td")[1].string
  gender = pdrtable.find_all("tr")[4].find_all("td")[1].string
  t = t + bib + ", " + gender + ", "

  # time splits
  srt = std = ""
  ftrt = fttd = ""
  oort = ootd = ""
  mbrt = mbtd = ""
  lhrt = lhtd = ""
  frt = ftd = ""
  for r in h.find_all("tr", class_="dataRow"):
    c = r.find_all("td")
    if c[0].string == "Start":
      srt = c[2].string.strip()
      std = c[3].string.strip()
    elif c[0].string == "Fire Tower":
      ftrt = c[2].string.strip()
      fttd = c[3].string.strip()
    elif c[0].string == "Highway OO":
      oort = c[2].string.strip()
      ootd = c[3].string.strip()
    elif c[0].string == "Mosquito Brook Rd":
      mbrt = c[2].string.strip()
      mbtd = c[3].string.strip()
    elif c[0].string == "Lake Hayward":
      lhrt = c[2].string.strip()
      lhtd = c[3].string.strip()
    elif c[0].string == "Finish":
      frt = c[2].string.strip()
      ftd = c[3].string.strip()
  t = t + srt + ", " + std + ", " + ftrt + ", " + fttd + ", " + oort + ", " + ootd + ", " + mbrt + ", " + mbtd + ", " + lhrt + ", " + lhtd + ", " + frt + ", " + ftd
#  print(t)
  file.write(t+"\n")



# here is the "program"
file = open("skateresults.csv","w")
link = "http://birkie.pttiming.com/results/2019/?page=1150&r_page=division&divID=1"
rcount = 0;
while True:
  raw_html = simple_get(link)
  html = BeautifulSoup(raw_html, 'html.parser')
  for row in html.find_all("tr", class_="dataRow"):
    rcount = rcount + 1
    cols = row.find_all("td")
    ind_link = "http://birkie.pttiming.com/results/2019/" + cols[4].find("a")["href"]
    print(rcount)
    get_splits(ind_link)
  next = html.find("a", string="Next 100")
  if next != None:
    link = "http://birkie.pttiming.com/" + next["href"]
  else:
    break
