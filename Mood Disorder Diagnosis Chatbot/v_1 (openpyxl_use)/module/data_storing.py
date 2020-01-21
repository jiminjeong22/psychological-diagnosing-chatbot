from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import datetime


class Data_Storing:
    def __init__(self):
        self.scope = ['https://spreadsheets.google.com/feeds',
                      'https://www.googleapis.com/auth/drive']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name('sentiment-8cb7cb82813d.json', self.scope)
        self.gc = gspread.authorize(self.credentials)
        self.sh = self.gc.open('Sentiment_Diagnosis')

    def next_available_row(self, worksheet):
        str_list = list(filter(None, worksheet.col_values(1)))  # fastest
        return str(len(str_list) + 1)

    def data_storing(self, question, text, pos, neg, mood, sleep_disorder, how_long, eating_disorder):
        now = datetime.now()

        if question == "mood":
            worksheet = self.sh.get_worksheet(0)
            next_row = self.next_available_row(worksheet)


        elif question == "sleep":
            worksheet = self.sh.get_worksheet(1)
            next_row = self.next_available_row(worksheet)

            worksheet.update_acell("C{}".format(next_row), how_long)
            worksheet.update_acell("D{}".format(next_row), sleep_disorder)


        else:
            worksheet = self.sh.get_worksheet(2)
            next_row = self.next_available_row(worksheet)
            worksheet.update_acell("A{}".format(next_row), str(now))
            worksheet.update_acell("B{}".format(next_row), text)
            worksheet.update_acell("C{}".format(next_row), eating_disorder)
            worksheet.update_acell("D{}".format(next_row), pos)
            worksheet.update_acell("E{}".format(next_row), neg)
            worksheet.update_acell("F{}".format(next_row), mood)

        worksheet.update_acell("A{}".format(next_row), str(now))
        worksheet.update_acell("B{}".format(next_row), text)
        worksheet.update_acell("C{}".format(next_row), pos)
        worksheet.update_acell("D{}".format(next_row), neg)
        worksheet.update_acell("E{}".format(next_row), mood)
