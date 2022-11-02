This isn't for scraping reviews, just the Firm name and URL data from a given profile page, it crawls for profiles through search results, the search results are gained using headers and params with requests, because this actually only access each page of results once you can fetch 10 profile pages within 1-5 seconds.
These profile pages can then be all put together and given to the data scrape script, though you'll probably need to update headers/proxies for that script separately if you get blocked.

The use order is:


load the webpage
>>>
go to the next page/find max page count
>>>
get your headers and params from network info
>>>
convert to python code and remove comments (it will break the text file if you dont)
>>>
copy that info (but not the name of the dictionary i.e headers =) into the respective text file
>>>
save this
>>>
glassdoorprofile.py
>>>>
check your output csv for duplicates/nulls
>>>>
feed to glassdoordata.py this csv file
>>>>
assuming you didnt have to restart this at some point you're now done and just have to clean the final output

The program can handle restarts you just have to keep note of where the program last finished and remove parts you've already scraped/crawled, if youre doing this you still need to give it the last page number for example 300, it will just ask you to give the page number you are beginning from.

Your params should look something like:

{
    'overall_rating_low': '3',
    'page': '1',
    'locId': '2',
    'locType': 'N',
    'locName': 'United Kingdom',
    'sector': '10005',
    'filterType': 'RATING_OVERALL',
}

Here "sector" filters by what business type and loctype and locname by where the business are located, it could be that the search link you are given doesn't return the above values.
In this case, if it is necessary simply add the missing location values yourself, or by removing and then adding the location to the filter yourself. The new sodar in network should now contain these values which you can use to add to params.
If the location is irrelevant your params should look like the above without any location data.

