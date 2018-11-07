# Parts Logger
#### Author: Drake Bell
To run this program...
1) 	Within a terminal navigate the folder 'Parts_Logger'
		cd /path/to/Parts_Logger

2)	Open up links.txt with a text editor and input whatever
	part links you want to scrape. For each website ensure your
	links are to the correct product page...

	Adafruit: Should be in the /product/ page
	SparkFun: Should be in the /products/ page
	Digikey: Should be in the /product-details/ page. 
	Grainger: Should be in the /product/ page. This one is a bit trickier
			  as you have to click on the item link, and then click on the
			  'View Product Details' in the lower left corner.
	McMaster: Should be in the www.mcmaster.com/xxxxx where xxxxx is the 
			  product identification number. This one is a bit tricker as
			  you have to click on the item link, and then choose 
			  "Product Details" which appears on the popup after clicking
			  the item link.
		
		*******************************************************************
		Note: Do not leave any blank / new lines in the links.txt. It 
		won't error out, but you'll get all 'None' values in the CSV file.
		*******************************************************************

3)	The program currently just APPENDS all new information onto the data.csv
	file each time it is ran. If you'd like to start fresh, simply delete the 
	data.csv file and it will repopulate for you upon execution

4)	To actually RUN this program, if you are in the Parts_Logger directory, then 
	just type...
	py parts_logger.py 
	
		*********************************************************************
		Note: Please wait for the script to finish before trying to view the
		information. It won't hurt if you do, but it just takes it a bit to 
		actually populate the information in the data.csv file.
		*********************************************************************
