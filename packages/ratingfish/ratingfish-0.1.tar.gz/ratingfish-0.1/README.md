# ratingfish
Python wrapper for RatingFish API

#### Install
```
pip3 install ratingfish
```

### Example
```Python
import os
import ratingfish

API_KEY = os.environ['RATINGFISH_API_KEY']

rf = ratingfish.RatingFish(api_key=API_KEY)
website = rf.website.get()
print(website)
```

## Classes and methods
```
RatingFish.website.get - get website data
RatingFish.agents.get - get agents data
RatingFish.agents.stats - get agents stats
```
