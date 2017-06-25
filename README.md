# r/travel Country and Karma Analytics

I started this project to get more hands-on experience with APIs, SQL and Tableau plots/stories. I was also excited to work with travel data and reddit's API. The code for this project could be easily adapted to get and store posts featuring title keywords in any subreddit.

### The Data

The goal of this project was to analyze trends in country mentions on r/travel. I narrowed the time frame to Jan 2013 - Jun 2017 so posts would be relatively recent.

#### Country Labels
The most important column in the data is the country label. I initially attempted to extract this feature from raw title strings using the geograpy library (based on NLTK), but the results were fairly inaccurate (ie 1,400 Italy mentions in the cities table, and 1,350 in the countries table...). My second approach was much more straightforward. I simply used reddit's special cloudsearch parameters in the API query to search 'title:country_name' for every country in the world (there are only 126!). One major casualty of this process was the United States. "US" seemed a little too generic of a search term, so I just left it at the full name. For the UK I used the abbreviation, full name, and 'Scotland.'

#### API Insecurity
Reddit's API is somewhat notorious for its post-getting limitations. There's a 1000-post cap on certain query results, yet the Python library has a [function that claims to get all the posts between two given epoch time stamps](http://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html#praw.models.Subreddit.submissions) and it seems to work. I ended using a sliding window ~3 months wide just to be safe, though I'm sure some things managed to slip through (not to mention all the posts with no country names in their titles!).

#### Meta Data
I also gathered each posts meta-data including the domain, 'link flair' (label), and score. These were useful for getting at popularity trends besides post volume.

I made the necessary conversions for each data type and put all the posts into a table in SQL. In total I got 34,000 records.

### Analysis

I had a good time linking a Tableau up to the SQL table and doing the rest of the work in Tableau's great UI. The final data story can be found in most of its interactive glory [here](https://public.tableau.com/profile/jay1053#!/vizhome/rtravelCountryandKarmaTrends/rTravelStory) on Tableau's public pages, and in mobile-ready static images [here](http://imgur.com/a/RfCac) on imgur.
