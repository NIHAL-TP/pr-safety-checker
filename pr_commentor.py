import requests
import sys
from trivy_parser import load_trivy_results, extract_findings, count_by_severity
from trivy_report_formatter import report_formatter
import os
from dotenv import load_dotenv
load_dotenv()


def post_comment(api,headers,trivy_comment):
    print("api:",api)
    response=requests.post(api,headers = headers,json={"body":trivy_comment})
    return response


if __name__ == "__main__":
    json_path=sys.argv[1]
    REPO = "pr-safety-checker"
    ISSUE_NUMBER = "1"
    trivy_data=load_trivy_results(json_path)
    findings=extract_findings(trivy_data)
    severity_count=count_by_severity(trivy_data)
    trivy_comment=report_formatter(findings,severity_count)
    username = os.getenv("GITHUB_USER")
    token = os.getenv("GITHUB_TOKEN")
    
    #response = post_comment(api,headers,comment)


