# Half Foods Data Scanner

My response to the Half Foods Take Home Project.

# Answer to Question 3

## If only some of the files in the customer purchase database are corrupt, how would you address this problem going forward?

Depending on the amount of files, it may be wise to loop through all the files and verify and fix the corruption using a script or something similar so that the files are all verified. The approach for this problems assumes that the single character corruption does not corrupt it into another active product type. If so, it may require domain knowledge and being able to validate the subtypes of the product type against a list.

## What if the database was extremely large?

If the database was large, it could check for corruption when the data is accessed and then updated, if this software is the only use case and it is not being used for any analytics. It would also be wise to insert the data into an SQL database, and then run queries with statistics to check all counts of product types, then use SQL to replace any product types that clearly don't fit.

## How do you prepare for future data corruptions?

It would depend on the economics and the nature of the data corruption. Along with investigating the cause of the data corruption, having backups of the data and performing regular integrity checks against the backups should ensure that no data corruption lingers for long. If the corruption occurs during transmission from the scanning machine to the database it would be a different strategy than if the database machine's hardware fails.
