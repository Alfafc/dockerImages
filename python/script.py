import requests
import random
import time
import json
import os
import string

translator = str.maketrans('', '', string.punctuation + u'¿"–-”“')

headers={
    'Pragma': 'no-cache',
    'Origin': 'https://my.aivo.co',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'es-AR,es;q=0.9,en-US;q=0.8,en;q=0.7,es-419;q=0.6',
    # Replace token and authorization for the appropiate values
    'X-Token': 'WkRneU4yWTJaREJpTm1GaU16RmxNbUUzWVRSaU0yWTBNRGMzTUdRMU9EST0=',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuaWNrbmFtZSI6ImFuYS5yYW1vcyIsIm5hbWUiOiJBbmEgUmFtb3MiLCJwaWN0dXJlIjoiaHR0cHM6Ly9zLmdyYXZhdGFyLmNvbS9hdmF0YXIvYzUzMzVlY2EyNzY4ZGYzZTU1MTI1OWY1MzY2OWVhYzc_cz00ODAmcj1wZyZkPWh0dHBzJTNBJTJGJTJGY2RuLmF1dGgwLmNvbSUyRmF2YXRhcnMlMkZhci5wbmciLCJ1cGRhdGVkX2F0IjoiMjAxOS0wNC0xNlQxODoyNTowOS4yMzZaIiwiZW1haWwiOiJhbmEucmFtb3NAY29ydS5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9haXZvY28uYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVjNDY1MzZmYTAzYjdhMzQ0ODI2NmU1YyIsImF1ZCI6IlJ4TjJaOUlCMWJobmdUQTYwMnh0VENRYVROSkRSVm04IiwiaWF0IjoxNTU1NDM5MTA5LCJleHAiOjE1NTU0NzUxMDl9.AQFI2-hUaLJ6GkJTwBEspX3FYdZLqiGFTQDd8c65soE',
    'Accept': 'application/json, text/plain, */*',
    'Cache-Control': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Connection': 'keep-alive',
    'Referer': 'https://my.aivo.co/content',
    'DNT': '1'
}

def get_groups():
    print('Getting groups')
    if not os.path.exists('groups'):
        os.makedirs('groups')
    for page in range(1, 50):
        print(f'Page {page}')
        url = f'https://api.aivo.co/api/v1/content/groups/search?from=1530748800&to=1533427199&feedback=&complements=&conditions=&channels=&tags=&active=&revision=&nested=&interactionsMin=&interactionsMax=&page={page}&orderBy=date&sort=desc&perpage=200'
        response = requests.get(url, headers=headers).text
        if not len(json.loads(response)['groups']):
            return
        with open(f'groups/groups_{page}.json', 'w', encoding='utf-8') as f:
            f.write(response)
    # print('Sleeping')
    # time.sleep(random.random() * 2.0 + 1.0)

def load_groups():
    groups = []
    for page in range(1, 50):
        file_name = f'groups/groups_{page}.json'
        if not os.path.exists(file_name):
            break
        with open(file_name, 'r', encoding='utf-8') as f:
            groups.extend(json.loads(f.read())['groups'])
    return groups

def parse_groups():
    print('Parsing groups')
    groups = load_groups()
    if not os.path.exists('content'):
        os.makedirs('content')
    pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=total).start()
    for index, group in enumerate(groups):
        pbar.update(index + 1)
        id = str(group['id'])
        headers['Referer'] = 'https://my.aivo.co/content/edit/' + id
        url = f'https://api.aivo.co/api/v1/content/groups/{id}'
        response = requests.get(url, headers=headers).json()
        url = f'https://api.aivo.co/api/v1/content/groups/{id}/patterns'
        response['full_patterns'] = requests.get(url, headers=headers).json()['patterns']
        with open(f'content/{id}.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(response))
    # time.sleep(random.random() * 1.0 + 1.0)

def clean(string):
    return string.translate(translator)

def build_tree():
    groups = load_groups()
    for index, group in enumerate(groups):
        id = str(group['id'])
        print(id)
        with open(f'content/{id}.json', 'r', encoding='utf-8') as f:
            content_text = f.read()
            content = json.loads(content_text)
            name = clean(content['name'])
            for tag in content['tags']:
                parent = tag['parent'].lower().replace('"', '').replace('\'', '').replace('¿', '').replace('?', '')
                parent = parent \
                    .replace('centro metropolitano de diseño', 'cmd') \
                    .replace('ministerio', 'min') \
                    .replace('secretaría', 'sec') \
                    .replace('secretaria', 'sec') \
                    .replace('buenos aires', 'bs as')
                path = [folder.strip() for folder in parent.split('/') if folder.strip()]
                # print(path)
                # if index == 100:
                # 	return
                directory = u'tree'
                for i, folder in enumerate(path):
                    filtered = folder
                    for prevfolder in path[:i]:
                        filtered = filtered.replace(prevfolder, '')
                    filtered = filtered.strip()
                    if filtered:
                        directory += '/' + filtered
                if not os.path.exists(directory):
                    # print(tag['parent'], directory)
                    os.makedirs(directory)

                full_name = f'{directory}/{name}'[:250].strip()
                with open(f'{full_name}.json', 'w', encoding='utf-8') as fw:
                    fw.write(content_text)


from progressbar import ProgressBar, Percentage, Bar

def get_subpatterns():
    if not os.path.exists('subpatterns'):
        os.makedirs('subpatterns')
    subpatterns = set()
    for group in load_groups():
        id = str(group['id'])
        with open(f'content/{id}.json', 'r', encoding='utf-8') as f:
            for pattern in json.loads(f.read())['full_patterns']:
                subpatterns.update([part['subpatternId'] for part in pattern['parts']])
    total = len(subpatterns)
    print('Found patterns: ', total)
    pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=total).start()

    for index, subpattern in enumerate(subpatterns):
        url = f'https://api.aivo.co/api/v1/content/subpatterns/{subpattern}/details'
        response = requests.get(url, headers=headers).text
        pbar.update(index + 1)
        with open(f'subpatterns/{subpattern}.json', 'w', encoding='utf-8') as f:
            f.write(response)
    pbar.finish()


get_groups()
parse_groups()
get_subpatterns()
# build_tree()
