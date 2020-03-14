# logs-to-sheet

A small program that uploads logs from logs.tf into a Google Sheet

## Setup

1. Download the repository and unzip it - https://github.com/irodionr/logs-to-sheet/archive/master.zip
2. Go to https://console.cloud.google.com/projectcreate and create a project (default parameters are fine)
3. Enable Google Sheets API - https://console.cloud.google.com/marketplace/details/google/sheets.googleapis.com
4. Create a service account (https://cloud.google.com/docs/authentication/getting-started), select `Project > Editor` role instead of `Project > Owner`, download a JSON file with your key
5. That JSON file should look similar to `creds.json` in this repository, copy contents of your JSON file into `creds.json` replacing everything in it (you can use any text editor)

## Usage

1. Open `config.json` and enter proper inputs instead of placeholder examples:  
  `sheet` - URL to available Google Sheet (make sheet publicly available or give access to `"client_email"` from `creds.json`)  
  `id` - your SteamID (you can find one on your ETF2L profile page, for example)  
  `logs` - any amount of comma-separated URLs to logs that you want to upload
2. Run `logs-to-sheet.exe` (or run `logs-to-sheet.py` directly from the command line if you have python installed)

Program will create `Logs` worksheet (or use an already existing one) and output the logs in the following format:  
```
| Date:   |
| Map:    |
| Result: |
| ID      | Player | Kills | KPM | Assists | APM | Deaths | DeathsPM | Damage | DPM | DT | DTM | Heals | HPM | KA/D | K/D | Airshots | Headshots | Backstabs | Captures
...
```

