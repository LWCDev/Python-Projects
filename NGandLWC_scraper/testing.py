link = 'www.testing.co.uk/page[1-10]'
pages = link.split('[', 1)[1].split(']')[0]
min_num = pages[0:pages.index('-')]
max_num = pages[pages.index('-')+1:]
web_range = range(int(min_num), int(max_num)+1, 1)
for k in web_range:
    web_url = link.replace('[', '').replace(']', '').replace(pages, str(k))
    print(web_url)