import pickle
import praw
import math
import MySQLdb
import unicodedata
import time

# Loading pickles
country_list = pickle.load(open('pkls/country_list.pkl', 'rb'))
rdt_secrets = pickle.load(open("secret_pickle/sec_dict.pkl", "rb"))

# character encodings
def asciify(st):
    if type(st) == unicode:
        st = unicodedata.normalize('NFKD', st).encode('ascii', 'ignore').strip()
    else:
        st = unicode(st, 'ascii', 'ignore')
        st = unicodedata.normalize('NFKD', st).encode('ascii', 'ignore').strip()
    return st


# Set up the Reddit API
print "Setting up Reddit API!"
reddit = praw.Reddit(client_id=rdt_secrets['client_id'],
                     client_secret=rdt_secrets['secret'],
                     user_agent=rdt_secrets['agent'])
rtravel = reddit.subreddit('travel')

# Setting up the Database
print "Initializing the Database Connection"

db = MySQLdb.connect(host="127.0.0.1",
                     user="pyuser",
                     passwd="password",
                     db="reddit",
                     port=4406)
cur = db.cursor()

# Declare some table meta-data and formatting helpers
col_types = {'country': 'varchar(100)',
             'title': 'varchar(301)',
             'name': 'varchar(100)',
             'score': 'int',
             'view_count': 'int',
             'created_utc': 'int',
             'domain': 'varchar(100)',
             'link_flair_text': 'varchar(100)',
             'date': 'datetime'}
fields = ['country', 'title', 'name', 'score', 'view_count', 'created_utc', 'domain',
          'link_flair_text', 'date']
api_fields = ['title', 'name', 'score', 'view_count', 'created_utc', 'domain',
              'link_flair_text']
limits = {'country': 100,
          'title': 301,
          'name': 100,
          'domain': 100,
          'link_flair_text': 50}
int_vars = ['score', 'view_count', 'created_utc']

# Chunk of code to delete the table and re-create it
INIT_TABLE = False
if INIT_TABLE:
    print "DROPPING AND REMAKING THE TABLE"
    # Table Deletion / Recreation
    cur.execute("DROP TABLE IF EXISTS TRAVEL_AGAIN")
    # construct the CREATE TABLE query
    sql = """CREATE TABLE TRAVEL_AGAIN (ID int NOT NULL AUTO_INCREMENT PRIMARY KEY,"""
    for key in fields:
        col_name = key.upper()
        sql = sql + " " + col_name + " " + col_types[key] + ","
    sql = sql[:-1] + ")"
    cur.execute(sql)

# Chunk of code to allow aliasing of a search-word to a country_name in database
# Set to false to use default country list
country_aliasing = True
country_alias_list = ['scotland', 'uk']
country_alias_name = 'United Kingdom'
if country_aliasing:
    country_list = country_alias_list

# Setting up the querying, unpacking and sql insertion loop
print "Entering the Hyperloop"

# Epoch calculations to set up the sliding-window API query
start, end = 1356998400, 1498184396
year_len = 31622400
frames_per_year = 3
frame_width = int(math.ceil(year_len / frames_per_year))
interval_count = int(math.ceil((end - start) / float(frame_width)))

# Iterate the loaded country names
for country in country_list:
    print "Searching for posts with: " + str(country)
    # initialize the sliding window, and cloud-search extra_query
    frame_end = start - 1
    title_query = "title:" + "'" + country.lower() + "'"
    # Iterate the sliding windows
    for i in range(interval_count):
        frame_start = frame_end + 1
        frame_end = frame_end + frame_width
        # Iterate the API responses
        for submission in rtravel.submissions(start=frame_start, end=frame_end, extra_query=title_query):
            if submission != 0:
                # initiate the list for db insertion (allow aliasing)
                if country_aliasing:
                    vals = [country_alias_name]
                else:
                    vals = [country]
                # unpack the API response
                for var in api_fields:
                    # treat ints for sql
                    if var in int_vars:
                        val = getattr(submission, var)
                        if val is None:
                            val = 0
                        val = int(val)
                    # treat strings for sql
                    else:
                        val = getattr(submission, var)
                        if val is None:
                            val = "NA"
                        else:
                            val = asciify(val)
                            lim = limits[var] - 1
                            val = val[0:lim]
                    # convert epoch int to sql datetime format
                    if var == 'created_utc':
                        stime = time.gmtime(val)
                        dt = time.strftime('%Y-%m-%d %H:%M:%S', stime)
                    # update row
                    vals.append(val)
                vals.append(dt)
                cur.execute("""INSERT INTO TRAVEL_AGAIN
                (country, title, name, score, view_count, created_utc, domain, link_flair_text, date) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                            tuple(vals))
                db.commit()
            # no posts in API response
            else:
                continue
    print "Finished " + str(country)

''' SQL code for converting fromt epoch int to date time in SQL (now implemented above)
# create datetime column and populate it with converted timestamp ints
# or just do these commands in mysql
sql = "alter table travel_again add column date datetime after created_utc"
cur.execute(sql)
db.commit()
sql = "update travel_again set date = FROM_UNIXTIME(created_utc)"
cur.execute(sql)
db.commit()
'''

# disconnect from the database
db.close()
