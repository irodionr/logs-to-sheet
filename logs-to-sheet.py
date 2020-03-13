import urllib.request, json, gspread, datetime
from oauth2client.service_account import ServiceAccountCredentials

def parse_log(link, steam_id):
    split_link = link.split('/')
    link = 'http://logs.tf/json/' + split_link[-1]

    url = urllib.request.urlopen(link)
    log = json.load(url)

    if steam_id in log['players']:
        team = log['players'][steam_id]['team']
        teammates = []

        for player_id in log['players']:
            if log['players'][player_id]['team'] == team:
                teammates.append(player_id)
        teammates.sort()

        logs_table = []
        logs_table.append(['Date:', datetime.datetime
            .fromtimestamp(log['info']['date']).strftime('%Y-%m-%d %H:%M:%S')])
        logs_table.append(['Map:', log['info']['map']])

        result = None
        enemy = None
        if team == 'Blue':
            enemy = 'Red'
        else:
            enemy = 'Blue'
        if log['teams'][team]['score'] > log['teams'][enemy]['score']:
            result = 'Win'
        elif log['teams'][team]['score'] < log['teams'][enemy]['score']:
            result = 'Loss'
        else:
            result = 'Tie'
        logs_table.append(['Result:', str(log['teams'][team]['score']) + '-'
            + str(log['teams'][enemy]['score']), result])

        logs_table.append(['ID', 'Player', 'Kills', 'KPM', 'Assists', 'APM',
                           'Deaths', 'DeathsPM', 'Damage', 'DPM', 'DT',
                           'DTM', 'Heals', 'HPM', 'KA/D', 'K/D',
                           'Airshots', 'Headshots', 'Backstabs', 'Captures'])

        for player_id in teammates:
            stats = log['players'][player_id]
            mins = log['length'] / 60
            row = []
            row.append(player_id)
            row.append(log['names'][player_id])
            row.append(stats['kills'])
            row.append(round(stats['kills'] / mins, 2))
            row.append(stats['assists'])
            row.append(round(stats['assists'] / mins, 2))
            row.append(stats['deaths'])
            row.append(round(stats['deaths'] / mins, 2))
            row.append(stats['dmg'])
            row.append(stats['dapm'])
            row.append(stats['dt'])
            row.append(round(stats['dt'] / mins, 2))
            row.append(stats['hr'])
            row.append(round(stats['hr'] / mins, 2))
            row.append(float(stats['kapd']))
            row.append(float(stats['kpd']))
            row.append(stats['as'])
            row.append(stats['headshots_hit'])
            row.append(stats['backstabs'])
            row.append(stats['cpc'])
            logs_table.append(row)
        
        return logs_table

def open_worksheet(link):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive.file',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(link)

    worksheets = sheet.worksheets()
    for ws in worksheets:
        if ws.title == 'Logs':
            return ws

    sheet.add_worksheet('Logs', 0, 0)
    return sheet.worksheet('Logs')

def add_to_sheet(log, sheet):
    sheet.insert_row([])
    index = 1
    for row in log:
        sheet.insert_row(row, index)
        index += 1

def main():
    config = json.load(open('config.json'))
    print('Steam ID: ' + config['id'])
    sheet = open_worksheet(config['sheet'])
    print('Google spreadsheet: ' + config['sheet'])

    count = 1
    for link in config['logs']:
        print('Log: ' + link)
        log = parse_log(link, config['id'])
        print('Uploading log (' + str(count) + '/' + str(len(config['logs']))
            + ') to spreadsheet...')
        add_to_sheet(log, sheet)
        count += 1
    
    print('Done!')

main()
