# upwork_xml_parser

https://www.upwork.com/jobs/~01ab12fc34bbc35c50

There are 25 zipped sample data files each representing a particular year that contains XML code.  
The XML code is consistent within each file but varies over the years of files.  
Each zipped  file contains about 4000 XML files that are concatenated together to make up 1 file.  

1. Group the individual files with the same xml code together in a directory and 
2. write python code that will unzip these similar files into a data directory and 
3. pull two pieces of data from the files and store in a dataframe:  
   
   - application year
   - application number
   
   There will be an application year (based on the application date (yearmonthday) (not unique) and a 
   unique application number for each of the 4000 entries in 1 file so pull all 
   application years and application numbers within each file. The XML identifying field code has changed over the 
   years though not every year.  
   
4. Save the dataframe into an excel file csv or tsv. 
   There is likely 4-7 various XML code variations over the years.  
   See example file attached. 
   What I request from potential programmers is a projected cost and deliverable date including the number hours you 
   see the task taking and your hourly rate or fixed rate.

# To Do:
 - Add routines to keep track of...