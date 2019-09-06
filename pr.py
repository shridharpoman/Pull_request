import argparse
import csv
import requests
import json
import pandas as pd
import os
import configparser

config = configparser.ConfigParser()
config.read("./github_cred.conf")
username = config.get('github', 'username')
password = config.get('github','password')
team_csv= config.get('team_csv','csv')
auth = None
state = 'closed'
fromdate=''
todate=''



def write_pull_request(r, csvout):
    """Parses JSON r and writes to CSV."""
    data=r.json()
    if r.status_code != 200:
        raise Exception(r.status_code)
    for fields in data['items']:
        #users = ', '.join([u['login'] for u in pulls['user']])
        #labels = fields['labels'][0]['name']
        labels = ', '.join([u['name'] for u in fields['labels']])
        date = fields['created_at'].split('T')[0]
        # Change the following line to write out additional fields
        csvout.writerow([fields['number'],fields['user']['login'], labels, fields['title'], fields['body'] , fields['state'], date,fields['html_url']])


def get_pull_request(name,author,fromdate,todate):
    """Requests pull_request from GitHub API and writes to CSV file."""
    url = 'https://api.github.com/search/issues?q=is:pr+repo:{}+state:{}+author:{}+created:{}..{}'.format(name, state,author,fromdate,todate)
    r = requests.get(url, auth=auth)
    
    
    csvfilename = '{}-pr.csv'.format(name.replace('/', '-'))
    with open(csvfilename, 'a', newline='') as csvfile:
        csvout = csv.writer(csvfile)
        csvout.writerow(['PR_id','Author','labels', 'Title', 'Comments' ,'State', 'Date', 'URL'])
        write_pull_request(r, csvout)

        # Multiple requests are required if r is paged
        if 'link' in r.headers:
            pages = {rel[6:-1]: url[url.index('<')+1:-1] for url, rel in
                     (link.split(';') for link in
                      r.headers['link'].split(','))}
            while 'last' in pages and 'next' in pages:
                pages = {rel[6:-1]: url[url.index('<')+1:-1] for url, rel in
                         (link.split(';') for link in
                          r.headers['link'].split(','))}
                r = requests.get(pages['next'], auth=auth)
                write_pull_request(r, csvout)
                if pages['next'] == pages['last']:
                    break


parser = argparse.ArgumentParser(description="Write GitHub repository pull_request "
                                             "to CSV file.")
parser.add_argument('repositories', nargs='+', help="Repository names, "
                    "formatted as 'username/repo'")
parser.add_argument('--all', action='store_true', help="Returns both open "
                    "and closed pull_request.")

parser.add_argument('fromdate')

parser.add_argument('todate')

#parser.add_argument('authors',help="Author name",nargs='+')                    
args = parser.parse_args()

test=pd.read_csv(team_csv)

a=test['Author'].tolist()

if args.all:
    state = 'all'

if args.fromdate:
    fromdate=args.fromdate

if args.todate:
    todate=args.todate    


auth = (username, password)
for repository in args.repositories:
    for i in a:
        author=i
        get_pull_request(repository,author,fromdate,todate)

            




    # for arg in args.authors:
    #     for author in a:
    #         args.authors=author