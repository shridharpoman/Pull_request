Install the dependencies with command 
# pip3 install -r requirements.txt


Add you github credentials to github_cred.conf file, if no permission to change the file add suitable permissions 
for Linux - sudo chmod 777 github_cred.conf

Then add the csv file of Authors like aut.csv,(keep in the same folder of our code ie. pr.py)
the csv file for authors is mentioned in github_cred.conf

Then run the python script as python # python ./pr.py organisation/repo fromdate todate ie
# python ./pr.py facebook/react 2018-09-04 2019-09-04

