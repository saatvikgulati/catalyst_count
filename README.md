## I have designed a login signup and register pages for the user

#### To install dependencies do-

```pip install -r requirements.txt```

Before running the server load the enviornment variables
by doing ```dotenv -e .env```

## The query builder screen has autocomplete feature-
As soon as you start typing it will give dropdown on the basis of what you have typed. 
It uses Django rest framework api to query data into the db.

### The user_list view-
Will allow other users to only delete if the other users that have logged in 30 days are non staff users that means super_users will be shown if they have logged in past 30 days but people cannot delete them

### The upload data
We can upload csv files which will be bulk inserted