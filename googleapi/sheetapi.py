# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# import pickle
# import os.path
#
# from dataclasses import dataclass
#
#
# @dataclass
# class GoogleSheetRequest:
#     spreadsheet_id: str = ""
#     sheet_name: str = ""
#     body: [] = ()
#     value_range: str = ""
#     input_option: str = "USER_INPUT"
#
#
# class GoogleService:
#
#     def __init__(self, credential_path, scope='https://www.googleapis.com/auth/spreadsheets'):
#         creds = None
#         if os.path.exists('token.pickle'):
#             with open('token.pickle', 'rb') as token:
#                 creds = pickle.load(token)
#         # If there are no (valid) credentials available, let the user log in.
#         if not creds or not creds.valid:
#             if creds and creds.expired and creds.refresh_token:
#                 creds.refresh(Request())
#             else:
#                 flow = InstalledAppFlow.from_client_secrets_file(credential_path, scope)
#                 creds = flow.run_local_server(port=8081)
#             # Save the credentials for the next run
#             with open('token.pickle', 'wb') as token:
#                 pickle.dump(creds, token)
#         self.service = build('sheets', 'v4', credentials=creds)
#
#     def read(self, sheet_request: GoogleSheetRequest):
#         return self.service.spreadsheets().values().get(spreadsheetId=sheet_request.spreadsheet_id,
#                                                  range=sheet_request.value_range).execute()
#
#     def append_values(self, sheet_request: GoogleSheetRequest):
#         # range_name = f'{sheet_name}:value_range'
#         self.service.spreadsheets().values().append(spreadsheetId=sheet_request.spreadsheet_id,
#                                                     range=sheet_request.value_range,
#                                                     body=sheet_request.body).execute()
#
#     def update(self, sheet_request: GoogleSheetRequest):
#         self.service.spreadsheets().values().update(spreadsheetId=sheet_request.spreadsheet_id,
#                                                     range=sheet_request.value_range,
#                                                     body=sheet_request.body).execute()
