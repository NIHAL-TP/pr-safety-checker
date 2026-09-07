import requests
import sys
from parser import load_trivy_results, extract_findings, count_by_severity
from report_formatter import report_formatter
import os
from dotenv import load_dotenv
load_dotenv()


def post_comment(api,headers,comment):
    response=requests.post(api,headers = headers,json={"body":comment})
    return response


if __name__ == "__main__":
    json_path=sys.argv[1]
    REPO = "pr-safety-checker"
    ISSUE_NUMBER = "1"
    trivy_data=load_trivy_results(json_path)
    findings=extract_findings(trivy_data)
    severity_count=count_by_severity(trivy_data)
    comment=report_formatter(findings,severity_count)
    username = os.getenv("GITHUB_USER")
    token = os.getenv("GITHUB_TOKEN")
    
    response = post_comment(api,headers,comment)


