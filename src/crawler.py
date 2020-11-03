import requests, sys
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def crawl(url, maxDepth, depth=0, visited=set([])):
	if maxDepth < depth:
		return None
	print('\t' * depth + url)
	try:
		parsed = urlparse(url)
		if not parsed[0].startswith('http'):
			return None
		site = requests.get(url)
		text = BeautifulSoup(site.text, 'lxml')
		hyperlinks = text.find_all('a')
		visited.add(url)
		toRemove = []
		links = []
		for i in range(len(hyperlinks)):
			index =  hyperlinks[i].find('href')
			if index == -1:
				toRemove.append(hyperlinks[i])
				continue
			links.append(str(hyperlinks[i])[index:])
		for j in toRemove:
			hyperlinks.pop(hyperlinks.index(j))

		for k in range(len(links)):
			index = links[k].find("href")
			if(index == -1):
				links.pop(k)
			else:
				links[k] = links[k][index + 6:].split('"')[0]
				if visited.__contains__(links[k]):
					continue
				if not links[k].startswith('http') and not links[k].startswith('#'):
						links[k] = 'http:/' + links[k]
				elif links[k].startswith('#'):
					continue
				visited.add(links[k])
				crawl(links[k], maxDepth, depth + 1, visited)
	except IndexError as index_error:
		print('\t' * depth + '\tindex went out of range')
		return None
	except requests.exceptions.ConnectionError:
		print('\t' * depth + "\tcouldn't connect")
	except Exception as e:
		visited.add(url)
		print(e)
		return None


if len(sys.argv) == 1 or len(sys.argv) > 3:
	print('Invalid number of arguments')
	print('crawler.py [Absolute URL] [MAX DEPTH]')
	exit()
if  not sys.argv[1].startswith("http"):
	print("URL must be absolute")
	exit()
url = sys.argv[1]
max_depth = 3
if len(sys.argv) == 3:
	if sys.argv[2].isnumeric():
		if int(sys.argv[2]) > 0:
			max_depth = int(sys.argv[2])


print(f"Crawling from {url} to a maximum distance of {max_depth} links")
crawl(url, max_depth)
