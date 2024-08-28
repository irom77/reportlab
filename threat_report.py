# from report import PDFGenerator # type: ignore
from connect import ProofpointAPIClient # type: ignore
from xmltags import replace_fstr # type: ignore
# from figures import figure1, figure2  # type: ignore
from omegaconf import OmegaConf # type: ignore
from datetime import datetime
import sys
import calendar

def between_dates(month):
    year = datetime.now().year
    month_num = datetime.strptime(month, '%B').month
    _, last_day = calendar.monthrange(year, month_num)
    return f"From {month} 1 to {last_day} {year}"


if __name__ == "__main__":
    conf = OmegaConf.load('configs/_threat_report.yml')
    print(conf.report.month)
    formatted_date = datetime.now().strftime('%B %d, %Y')
    date_range = between_dates(conf.report.month)
    print(f"Date range: {date_range}")
    client = ProofpointAPIClient()
    # result=client.messages_blocked()
    # print(result)
    print(between_dates(conf.month))
