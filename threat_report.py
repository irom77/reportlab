# from report import PDFGenerator # type: ignore
from connect import ProofpointAPIClient # type: ignore
from xmltags import replace_fstr # type: ignore
# from figures import figure1, figure2  # type: ignore
from omegaconf import OmegaConf # type: ignore
from datetime import datetime
import sys


if __name__ == "__main__":
    conf = OmegaConf.load('configs/_threat_report.yml')
    print(conf.report.month)
    formatted_date=datetime.now().strftime('%B %d, %Y')
    client = ProofpointAPIClient()
    # result=client.messages_blocked()
    # print(result)