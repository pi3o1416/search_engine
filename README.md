# search_engine
In this project we have a SearchHistory model in the search_history app that stores user search data like search text, search time, search results etc. 
We have a model KeywordOccurrences to store total occurrences of keywords on a particular date. keywords occurrences will generate automatically based on search text.
we applied BeautifulSoup and re to remove noisy data and punctuations, we applied the krovetz Stemming algorithm to extract word roots. we only use nouns to store
in the KeywordOccurrence model. 

Available search histories can be seen in "/history/list/" url. django Pagination with 3 items per page is used to display search history. 
Filtering is also available for search history lists.
We use ajax methodology to make callbacks.

