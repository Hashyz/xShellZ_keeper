import requests
import bs4
import time
import warnings
from urllib3.exceptions import InsecureRequestWarning
warnings.filterwarnings("ignore", category=InsecureRequestWarning)
# warnings.resetwarnings()
class xShellz:
  def __init__(self,username,password):
    self.username = username
    self.password = password
    self.url = "https://www.xshellz.com/"
    self.xsrf = None
    self.xshellz_session = None

  def getXsrf(self):
    res1 = requests.get(self.url,headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    })
    xsrf = res1.cookies.get_dict().get("XSRF-TOKEN")
    xshellz_session = res1.cookies.get_dict().get("xshellz_session")
    return {"xsrf":xsrf,"xshellz_session":xshellz_session}

  def login(self):
    raw = self.getXsrf()
    xsrf = raw.get("xsrf")
    xshellz_session = raw.get("xshellz_session")

    loginUrl = "https://www.xshellz.com/ajax/login"
    res2 = requests.post(loginUrl,json={"remember":True,
                                "username":self.username,"password":self.password},
                  headers={"X-Xsrf-Token":xsrf.replace("%3D",""),
                            # "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
                            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
                            
                            "Content-Type": "application/json;charset=UTF-8",
                            "Accept": "application/json, text/plain, */*"
                            },
                  cookies={"xshellz_session":xshellz_session})

    if res2.json().get("success"):
      xsrf = res2.cookies.get_dict().get("XSRF-TOKEN")
      xshellz_session = res2.cookies.get_dict().get("xshellz_session")
      self.xsrf = xsrf
      self.xshellz_session = xshellz_session
      print("Login Success!")
      return 1
    else:
      print(res2.json())
      print("Login Failed!")
      return 0
    # return {"xsrf":xsrf,"xshellz_session":xshellz_session}
 
  def getId(self,output=True):
    if self.xsrf == None or self.xshellz_session == None:
      print("You need to Login.")
      return 0
    res3 = requests.get("https://www.xshellz.com/",cookies={"XSRF-TOKEN":self.xsrf.replace("%3D","="),"xshellz_session":self.xshellz_session},
              verify=False,allow_redirects=True)
    href = bs4.BeautifulSoup(res3.text,'html.parser').find("tbody").find("a")['href']
    sshID = href.split("/")[-1]
    if output:print(f"SSH ID : {sshID}")
    return sshID
  
  def keep(self,output=True):
    sshID = self.getId()
    if sshID == 0:
      if output:print("Get ID Error!")
      return 0
    if self.xsrf == None or self.xshellz_session == None:
      if output:print("You need to Login.")
      return 0
    urlKeep = "https://www.xshellz.com/ajax/shell/keep"
    res4 = requests.post(urlKeep,json={"opid":sshID},
                headers={"X-Xsrf-Token":self.xsrf.replace("%3D","="),
                          # "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
                          "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
                          
                          "Content-Type": "application/json;charset=UTF-8",
                          "Accept": "application/json, text/plain, */*"
                          },
                cookies={"xshellz_session":self.xshellz_session}
                )
  
    if res4.json().get("success"):
      if output:print(res4.json().get("msg"))
      return 1
    else:
      print(res4.json().get("msg"))
      return 0

if __name__ == "__main__":
  username,password = "xxxx","xxxx"
  x = xShellz(username,password)
  x.login()
  # x.getId()#shell id
  x.keep()#Keep
