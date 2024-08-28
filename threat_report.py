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
    first_day = calendar.month_name[month_num]
    return f"From {first_day} to {last_day} {year}"


if __name__ == "__main__":
    conf = OmegaConf.load('configs/_threat_report.yml')
    # print(conf.report.month)
    formatted_date = datetime.now().strftime('%B %d, %Y')
    date_range = between_dates(conf.report.month)
    print(f"Date range: {date_range}")
    
    # Update the configuration
    conf.figure1.between_dates = date_range
    OmegaConf.save(conf, 'configs/_threat_report.yml')
    
    client = ProofpointAPIClient(conf)
    inbound_count = client.inbound_messages()
    print(f"Total inbound messages: {inbound_count}")
    # result=client.messages_blocked()
    # print(result)
