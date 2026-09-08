from parser import load_trivy_results,extract_findings,count_by_severity,get_severity_rank
from report_formatter import report_formatter
from pr_commentor import post_comment
import os
import sys
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    REPO="pr-safety-checker"
    data=sys.argv[1]
    trivy_data=load_trivy_results(data)
    severity_count=count_by_severity(trivy_data)
    findings=extract_findings(trivy_data)
    #print(findings)
    severity_rank = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    sorted_findings = sorted(findings, key=get_severity_rank)
    formatted_report=report_formatter(sorted_findings,severity_count)
    ISSUE_NUMBER=os.getenv("ISSUE_NUMBER")
    username=os.getenv("GITHUB_USER")
    token=os.getenv("GITHUB_TOKEN")
    print("ISSUE_NUMBER:", repr(ISSUE_NUMBER))
    print("username:", repr(username))
    print("token:", repr(token))
    api=f"https://api.github.com/repos/{username}/{REPO}/issues/{ISSUE_NUMBER}/comments"
    headers = {"Authorization": f"Bearer {token}"}
    #print(sorted_findings)
    #print(formatted_report)
    response=post_comment(api,headers,formatted_report)
    print(response.status_code)
    print(response.text)
    print("Token length:", len(token) if token else "None")
    print("Token starts with:", token[:4] if token else "None")
