from parser import load_trivy_results,extract_findings,count_by_severity
from report_formatter import report_formatter
from pr_commentor import post_comment
import os
import sys
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    REPO="pr-safety-checker"
    ISSUE_NUMBER=os.getenv("ISSUE_NUMBER")
    data=sys.argv[1]
    trivy_data=load_trivy_results(data)
    severity_count=count_by_severity(trivy_data)
    findings=extract_findings(trivy_data)
    formatted_report=report_formatter(findings,severity_count)
    username=os.getenv("GITHUB_USER")
    token=os.getenv("GITHUB_TOKEN")
    api=f"https://api.github.com/repos/{username}/{REPO}/issues/{ISSUE_NUMBER}/comments"
    headers = {"Authorization": f"Bearer {token}"}
    response=post_comment(api,headers,formatted_report)
    print(response.status_code)
