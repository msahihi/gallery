import os
from bs4 import BeautifulSoup, NavigableString
from bs4 import Comment

root = os.getcwd()
target_path = root+"/images"


file = open("index.html","r")
webpage = file.read()
soup = BeautifulSoup(webpage,'html.parser')
get_target_div = soup.find('div',{'id':'lightgallery'})
photo_list = [photos['href'].replace('images/','').lower() for photos in get_target_div.find_all('a')]
# print(photo_list)
pointer = soup.find('div', {'id': 'lightgallery'})
for dirName, subdirList, fileList in os.walk(target_path, topdown=False):
    rel_dir = os.path.relpath(dirName, target_path)
    if rel_dir.startswith('.'):
        continue
    comment_tag = Comment(" "+rel_dir.upper()+" ")
    pointer.append(comment_tag)
    print('=== %s ===' % comment_tag)
    for fname in fileList:

        if fname.startswith('.'):
            continue
        if "thumb-" in fname:
            continue
        if fname.lower() not in photo_list:
            new_soup = BeautifulSoup("", "html.parser")
            new_tag = new_soup.new_tag("a",attrs={'class':"grid-item", 'href':"images/"+rel_dir+"/"+fname})
            new_soup.append(new_tag)

            new_tag = new_soup.new_tag("img", attrs={'src':"images/"+rel_dir+"/thumb-"+fname})
            new_soup.a.append(new_tag)

            new_tag = new_soup.new_tag("div", attrs={'class':"demo-gallery-poster"})
            new_soup.a.append(new_tag)

            new_tag = new_soup.new_tag("img", attrs={'src':"static/img/zoom.png"})
            new_soup.a.div.append(new_tag)
            pointer.append(new_soup.a)
            print('[+] %s' % fname)


html = soup.prettify("utf-8")
with open("new.html", "wb") as file:
    file.write(html)
