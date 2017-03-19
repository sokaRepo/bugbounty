import requests
import re
from bs4 import BeautifulSoup
import time
import sqlite3
import json

def conn_sqlite():
	conn = sqlite3.connect('dashboard3.sqlite')
	return conn, conn.cursor()

def check_vuln_lab():
	text = requests.get("https://www.vulnerability-lab.com/list-of-bug-bounty-programs.php").text
	find = re.findall(r"\"((http|https)://(.*?))\" target=\"_blank\">([a-zA-Z0-9-. -\(-\-&)]+)</a>", text)
	conn, cursor = conn_sqlite()
	nb_programs_before = cursor.execute("SELECT COUNT(*) FROM programs").fetchone()[0]

	for f in find:
		if not 'vuln-lab' in f[0] and not 'vulnerability-lab' in f[0]:
			cursor.execute("insert into programs(company, link, lab, date) select ?, ?, 'vuln-lab', ? where not exists(select 1 from programs where lower(company) = ? or link = ?);", (f[3], f[0], int(time.time()), f[3].lower(), f[0]))
	conn.commit()
	conn.close()
	
def check_bugcrowd():
	src = requests.get('https://bugcrowd.com/list-of-bug-bounty-programs').text
	soup = BeautifulSoup(src, "html.parser")
	programs = soup.findAll('a', {'class':'tracked'})
	conn, cursor = conn_sqlite()
	for prog in programs:
		cursor.execute("insert into programs(company, link, lab, date) select ?, ?, 'bugcrowd', ? where not exists(select 1 from programs where lower(company) = ? or link = ?);", (prog.text, prog.get('href'), int(time.time()), prog.text.lower(), prog.get('href')))
	conn.commit()
	conn.close()

def check_hackerone():
	headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
	'X-Requested-With': 'XMLHttpRequest'
	}
	src = requests.get('https://hackerone.com/programs/search?query=bounties%3Ayes&sort=name%3Aascending&limit=1000').text
	try:
		src_json = json.loads(src)
	except:
		print "Error while loading json"
		return
	programs = src_json['results']
	conn, cursor = conn_sqlite()
	for program in programs:
		cursor.execute("insert into programs(company, link, lab, date) select ?, ?, 'hackerone', ? where not exists(select 1 from programs where lower(company) = ? or link = ?);", (program['name'], 'https://hackerone.com'+program['url'], int(time.time()), program['name'].lower(), 'https://hackerone.com'+program['url']))
	conn.commit()
	conn.close()

def check_bountyfactory():
	src = requests.get('https://bountyfactory.io/programs').text
	soup = BeautifulSoup(src, "html.parser")
	programs = soup.findAll('div', {'class':'panel-body'})
	conn, cursor = conn_sqlite()
	for program in programs:
		try:
			link = program.find('a', {'class':'media-heading text-semibold'}).get('href')
			link = "https://bountyfactory.io" + link
			name = program.find('p', {'class':'text-size-small'}).text
			cursor.execute("insert into programs(company, link, lab, date) select ?, ?, 'bountyfactory', ? where not exists(select 1 from programs where lower(company) = ? or link = ?);", (name, link, int(time.time()), name.lower(), link))
		except:
			pass	
	conn.commit()
	conn.close()







if __name__ == '__main__':
	print 'Check vuln-lab...',
	check_vuln_lab()
	print ' OK'
	print 'Check BugCrowd...',
	check_bugcrowd()
	print ' OK'
	print 'Check HackerOne...',
	check_hackerone()
	print ' OK'
	print 'Check BountyFactory...',
	check_bountyfactory()
	print ' OK'
