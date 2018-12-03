# DuckDuckGo Filter Bubble Study (2018)

Python scripts used to analyse Google search results for the 2018 filter bubble study.
This assumes Python version 2.7.


## Usage

To count domain occurrences within organic links (i.e. excluding infoboxes):
```
$ python count_domains.py
```

To count variations of the search results and infoboxes:
```
$ python count_variations.py
```

To calculate the average differences ([edit distances](https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance)) of participants' search results:
```
$ python measure_difference.py
```


## Dependencies

[pyxDamerauLevenshtein](https://pypi.org/project/pyxDamerauLevenshtein/) >= 1.5


## Reference

See also the spreadsheets containing all data from the study here:
* https://duckduckgo.com/download/duckduckgo-filter-bubble-study-2018_participants.xls
* https://duckduckgo.com/download/duckduckgo-filter-bubble-study-2018_raw-search-results.xls
