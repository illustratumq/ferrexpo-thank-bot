import string
import sys
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

from app.misc.utils import now

if sys.version_info.major == 3 and sys.version_info.minor >= 10:
    import collections

    setattr(collections, "MutableMapping", collections.abc.MutableMapping)


class GoogleSheet:
    credentials = Path('app', 'database', 'googlesheet', 'credentials.json')
    # credentials = 'credentials.json'
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive',
    ]

    def __init__(self):
        self.service = self.authorization

    @classmethod
    def env(cls):
        return GoogleSheet()

    @property
    def authorization(self):
        credentials = service_account.Credentials.from_service_account_file(self.credentials, scopes=self.scopes)
        return build('sheets', 'v4', credentials=credentials)

    def update_cells(self, coordinates: str, values, spreadsheet_id: str):
        data = [{
            'range': coordinates,
            'values': values
        }]
        body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
        }
        return self.service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body
        ).execute()

    def read_cells(self, spreadsheet_id: str, coordinates: str):
        return self.service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=coordinates
        ).execute()['values']

    def write_event(self, spreadsheet_id: str, action: str, sender_name: str, getter_name: str,
                    points: int, val: str, message: str, sheet_name: str = 'Registration'):
        data = now().strftime('%d %B %y')
        last_cell_index = len(self.read_cells(spreadsheet_id, f'{sheet_name}!A:B'))
        write_data = [action, sender_name, getter_name, points, data, val, message]
        second_range_letter = list(string.ascii_uppercase)[len(write_data)-1]
        self.update_cells(
            coordinates=f'{sheet_name}!A{last_cell_index + 1}:{second_range_letter}{last_cell_index + 1}',
            values=[write_data],
            spreadsheet_id=spreadsheet_id
        )

    def get_auth_data(self, spreadsheet_id: str):
        result = self.get_users_data(spreadsheet_id)
        auth_data_lst = []
        for user in result:
            full_name = user[0]
            auth_data = user[1]
            if auth_data not in auth_data_lst:
                auth_data_lst.append((full_name, auth_data))
        return auth_data_lst

    def get_users_data(self, spreadsheet_id: str):
        result = self.service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='A3:C').execute()['values']
        answer = []
        for row in result:
            if len(row) == 3:
                name, auth_data, command = row
                answer.append((name, auth_data, command))
        return answer

    def get_commands(self, spreadsheet_id: str):
        result = self.get_users_data(spreadsheet_id)
        commands = []
        for user in result:
            command = user[-1]
            if command not in commands:
                commands.append(command)
        return commands

    def get_user(self, spreadsheet_id: str, auth_data: str) -> tuple:
        result = self.get_users_data(spreadsheet_id)
        for user in result:
            auth_data_user = str(user[1])
            if auth_data_user.isnumeric():
                auth_data = auth_data.replace('+', '')
                auth_data_user = auth_data_user.replace('+', '')
                if auth_data_user == auth_data:
                    return user
                auth_data_user = auth_data_user.replace('38', '')
                if auth_data_user == auth_data:
                    return user
            elif auth_data_user == auth_data:
                return user


# for i in GoogleSheet().get_users_data('1bQeq3y-eNrs1MBTKLVV-wPtP7Qd9j48LOlwnZE2cCcw'):
#     print(' '.join(i[::-1][1:]))
