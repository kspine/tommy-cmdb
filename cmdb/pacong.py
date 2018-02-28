from bs4 import BeautifulSoup
import requests,pandas

req=requests.get("https://www.kuaidaili.com/free/inha/5/")
x=[]
shop=BeautifulSoup(req.text,'html.parser')
#for i in shop.find_all("td",{"data-title":"IP"}):
#    print (i.text)
for i in shop.find_all("tr"):
    try:
        IP=i.find_all("td",{"data-title":"IP"})[0].text
        PORT=i.find_all("td",{"data-title":"PORT"})[0].text
        leixing = i.find_all("td", {"data-title": "类型"})[0].text
        x.append((IP,PORT,leixing))
    except Exception:
        pass
print(x)

#for i in shop.select("tr"):
 #   try:
  #      print(i.select("td")[0].text)
  #  except:
  #      print("ng")
#for i in shop.select("tr"):
#    print(i.select("td")[0])

#pad=pandas.read_html("https://www.kuaidaili.com/free/inha/5/")
#print(pad)

#for i in pad:
 #   print('###',i)