To run a program you need a text file, where every line is in format:

url regexp

Program will continuously connect to urls, apply respective regular expressions on
fetched htmls and write obtained result to another text file in format:

time of connection started | url | time of html was fetched as text/time of error occured in connection | results of applied regexp/"cannot connect" in the case of error

External dependencies can be installed with pip install -r requirements.txt  

Program is run with main.py (in scripts folder):

python main.py file_in file_out,

where file_in is the name of file with urls and regexps, and file_out is the name of file where results are written.

To run tests: pytest test.py  


