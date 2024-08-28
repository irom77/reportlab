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
    print(f"Total inbound messages for {conf.report.month}: {inbound_count}")
    
    # Add debug information
    now = datetime.now()
    report_month = datetime.strptime(conf.report.month, '%B')
    year = now.year if report_month.month <= now.month else now.year - 1
    month = report_month.month
    _, last_day = calendar.monthrange(year, month)
    start_date = datetime(year, month, 1)
    end_date = min(datetime(year, month, last_day, 23, 59, 59), now)
    print(f"Debug: Calculated - Start date: {start_date}, End date: {end_date}")
    print(f"Debug: Calculated - Seconds since start: {int((end_date - start_date).total_seconds())}")
    
    # Update the configuration with the inbound count
    conf.figure1.inbound_messages = inbound_count
    OmegaConf.save(conf, 'configs/_threat_report.yml')

    print(f"\nDebug: Current date and time: {now}")
    print(f"Debug: Report month: {conf.report.month}")
    print(f"Debug: Year used for calculation: {year}")
    
    # result=client.messages_blocked()
    # print(result)
