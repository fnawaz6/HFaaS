

bugs: 
- working with Period index is not convenient. Consider changing it to datetime, freq
- AAPL shows date at the beginning of quarter, how to deal with it? (no problem)
- SEC does not have recent quarter data (!!!!!!!!!!!!!!!!!!!!!!)
- Some dates are not valid, greater than 2017 (Done)
- Coreg=null means consolidated company and we want this only (DONE)
- Some statements are not classfied. Drop them (Done)

- take care of item vs tag, edit it on sec2df and on tag2items (tag is tag, item is plabel, no need for tag dataset)
- tlabel as item is not good, change it to tag
- Annual or Yearly:
    - All are Annual

to do:
- download
- match
    - match to standard
    - cut off
    - do all years
- estimate
- prepare
- contact


- stmt is not in tag2item
- tag2item has no name (size)
- tag2item has NaN for missings
