#!/usr/bin/python
import re, sys, os, cookielib
import mechanize, rarfile
from BeautifulSoup import BeautifulSoup

def getmediaUrl(queryname):
    query = "site:divxplanet.com inurl:sub/m inurl:%s" % (queryname.replace(" ", "-"))
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    # br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # User-Agent (this is cheating, ok?)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    br.open("http://www.google.com")
    # Select the search box and search for 'foo'
    br.select_form( 'f' )
    br.form[ 'q' ] = query
    br.submit()
    page = br.response().read()
    soup = BeautifulSoup(page)

    linkdictionary = []
    query.replace(" ", "-")
    for li in soup.findAll('li', attrs={'class':'g'}):
        sLink = li.find('a')
        sSpan = li.find('span', attrs={'class':'st'})
        if sLink:
            linkurl = re.search(r"\/url\?q=(http:\/\/divxplanet.com\/sub\/m\/[0-9]{3,8}\/.*.\.html).*", sLink["href"])
            if linkurl:
                linkdictionary.append({"text": sSpan.contents, "name": queryname, "url": linkurl.group(1)})
    if len(linkdictionary) == 1:
        return linkdictionary[0]["url"]
    else:
        i = 0
        for l in linkdictionary:
            print i, l["url"]
            print l["text"]
            i += 1
        j = raw_input("Hangi Dizi?")
        return linkdictionary[int(j)]["url"]

def search_subtitles(title, season, episode): #standard input
    # Build an adequate string according to media type
    tvurl = getmediaUrl(title)
    print "looking at", tvurl
    divpname = re.search(r"http:\/\/divxplanet.com\/sub\/m\/[0-9]{3,8}\/(.*.)\.html", tvurl).group(1)
    season = int(season)
    episode = int(episode)
    # Browser
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    # br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # User-Agent (this is cheating, ok?)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    url = br.open(tvurl)
    html = url.read()
    soup = BeautifulSoup(html)
    subtitles_list = []
    i = 0
    # /sub/s/281212/Hannibal.html
    for link in soup.findAll('a', href=re.compile("\/sub\/s\/.*.\/%s.html" % divpname)):
        addr = link.get('href')
        info = link.parent.parent.nextSibling.nextSibling.findAll("td", colspan="3")
        if info:
            tse = info[0].div.findAll("b", text="%d" % season)
            tep = info[0].div.findAll("b", text="%02d" % episode)
            lantext = link.parent.find("br")
            lan = link.parent.parent.findAll("img", title=re.compile("^.*. (subtitle|altyazi)"))
            if tse and tep and lan and lantext:
                language = lan[0]["title"]
                if language[0] == "e":
                    language = "English"
                    lan_short = "en"
                else:
                    language = "Turkish"
                    lan_short = "tr"
                subtitles_list.append({'link'    : addr,
                                 'movie'         : title,
                                 'description'   : "%s" % (info[1].contents[0]),
                                 'filename'      : "%s S%02dE%02d.%s" % (title, season, episode, lan_short),
                                 'language_flag' : "flags/%s.gif" % lan_short,
                                 'language_name' : language,
                                 'sync'          : False,
                                 'rating'        : "0" })
    br.close()
    return subtitles_list


def download_subtitles (subtitles_list, pos): #standard input
    packed = True
    dlurl = "http://divxplanet.com%s" % subtitles_list[pos][ "link" ]
    language = subtitles_list[pos]["language_name"]
    # Browser
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    # br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # User-Agent (this is cheating, ok?)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    html = br.open(dlurl).read()
    br.select_form(name="dlform")
    br.submit()
    f = open(subtitles_list[pos]["filename"] + ".rar", "w")
    f.write(br.response().get_data())
    f.close()
    rf = rarfile.RarFile(subtitles_list[pos]["filename"] + ".rar")
    for r in rf.infolist():
        if "srt" in r.filename or "sub" in r.filename:
            rf.extract(r)
            print "Downloaded: ", r.filename
    os.remove(subtitles_list[pos]["filename"] + ".rar")
    br.close()

def main(argv):
    if argv:
        if len(argv) == 3:
            season = int(argv[1])
            episode = int(argv[2])
            if (season > 0 and episode > 0):
                sublist = search_subtitles(argv[0], season, episode)
                i = 0
                for sub in sublist:
                    print i, sub["language_name"], sub["description"]
                    i += 1
                dlsub = raw_input("Hangi Altyazi?")
                download_subtitles(sublist, int(dlsub))
        else:
            print "Kullanim: python dldp.py 'Dizi Adi' sezon_no bolum_no"
            print "Ornek: python dp.py 'game of thrones' 3 3"
    else:
        print "Kullanim: python dldp.py 'Dizi Adi' sezon_no bolum_no"
        print "Ornek: python dp.py 'game of thrones' 3 3"

if __name__ == "__main__":
   main(sys.argv[1:])

