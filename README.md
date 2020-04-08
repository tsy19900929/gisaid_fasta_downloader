# gisaid_fasta_downloader
a tool for downloading fasta from gisaid, is flexible to retrieve newest sequences instead of the whole database.
## a best practice tested on win10 
* [firefox 74.0.1 (64 位)](http://www.firefox.com.cn/)  
* [geckodriver 0.26.0](https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-win64.zip)  
* [python 3.8.2](https://www.python.org/ftp/python/3.8.2/python-3.8.2.exe)  
* ```pip install selenium==3.141.0```
## usage example
1. filter Accession ID from [gisaid_cov2020_acknowledgement_table.xls](https://www.epicov.org/epi3/frontend)
2. ```python gisaid_fasta_downloader.py -u user -p pass -l accession_id_list```
3. check fasta files in working directory
## screenshot
![img](https://github.com/tsy19900929/gisaid_fasta_downloader/blob/master/example.gif)





