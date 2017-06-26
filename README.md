# r/travel Country and Karma Analytics

I started this project to get more hands-on experience with APIs, SQL and Tableau plots/stories. I was also excited to work with travel data and reddit's API. The code for this project could easily be adapted to get and store posts with title keywords from any subreddit.
### The Data

The goal of this project was to analyze trends in country mentions on r/travel. I narrowed the time frame to Jan 2013 - Jun 2017 so posts would be relatively recent.

#### Country Labels
The most important column was the country name. I initially attempted to extract this feature from raw title strings using the geograpy library (based on NLTK), but the results were fairly inaccurate (ie 1,400 Italy mentions in the cities table, and 1,350 Italy mentions in the countries table...). My second approach was much more straightforward, but ignored more posts: I used reddit's special cloudsearch parameters in the API query to search 'title:country_name' for each of the 126 countries in the world. The script took under 10 minutes to complete, and the run time was mostly a result of Reddit's API throttling request rates. I considered adding the top 10 cities in each contry for more robust detection, but 34,000 results felt like enough.

One major casualty of this process was the United States. I was hesitant to use 'us' as a search term, so I just left it at the full name. For the UK I decided it was safe to use the abbreviation, and ran additional queries using the 'United Kingdom', and 'Scotland' as aliases. 

#### API Result Limit?
Reddit's API is somewhat notorious for its post-getting limitations. There's a ~1000-post cap on certain query results, yet the PRAW Python library has a [function that claims to get all the posts between two given epoch time stamps](http://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html#praw.models.Subreddit.submissions) and it seems to work way beyond 1000. I ended using a sliding window ~3 months wide just to be safe, though I'm sure some things managed to slip through (not to mention all the posts with no country names in their titles!).

#### Meta Data
I also gathered some meta-data from each post. These features included the domain, 'link flair' (label), and score. Score in particular was a fun way to look at country popularity, and answer questions about how to optimize posting practices for score (spoiler: it's a 6:00 UTC image post of a some-what unusual destination (like Slovenia) hosted on reddit's native image service).

#### TL:DR
I got the country, datetime, domain, flair, and score from 34,000 r/travel posts and put them in SQL.

### Analysis

I had a good time linking Tableau up to the SQL table and doing the rest of the work in Tableau's great UI. The final data story can be found in most of its interactive glory [here](https://public.tableau.com/profile/jay1053#!/vizhome/rtravelCountryandKarmaTrends/rTravelStory) on Tableau's public pages, and in mobile-ready static images [here](http://imgur.com/a/RfCac) on imgur.
