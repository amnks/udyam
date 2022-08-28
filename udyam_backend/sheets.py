import gspread
from oauth2client.service_account import ServiceAccountCredentials
from authentication.models import User

def addtosheet(sheetname, teamslist):
	scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
	creds = ServiceAccountCredentials.from_json_keyfile_name("udyam_backend/creds.json", scope)
	client = gspread.authorize(creds)
	sheet = client.open(sheetname).sheet1

	sheet.delete_rows(2, sheet.row_count)

	rows=[]
	rows.append(["Serial No", "Team Name", "", "", "Team Leader", "", "", "Member 2", "", "", "Member 3"])
	i=1

	for team in teamslist:
		rows.extend([["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"], [str(i), team.team_name, "", "", team.Team_leader, "", "", team.member1, "", "", team.member2]])
		i=i+1

	sheet.append_rows(rows)


def appendtosheet(sheetname, team):
	
	scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
	creds = ServiceAccountCredentials.from_json_keyfile_name("udyam_backend/creds.json", scope)
	client = gspread.authorize(creds)
	sheet = client.open(sheetname).sheet1

	i = int((sheet.row_count+1)/2)
	rows = [["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"], [str(i), team.team_name, "", "", team.Team_leader, "", "", team.member1, "", "", team.member2]]
	sheet.append_rows(rows)
