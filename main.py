from parser import load_trivy_results,extract_findings,count_by_severity
from report_formatter import report_formatter,get_severity_rank,findings_to_show
from pr_commentor import post_comment
import os
import sys
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    REPO="pr-safety-checker"
    ISSUE_NUMBER=os.getenv("ISSUE_NUMBER")
    username=os.getenv("GITHUB_USER")
    token=os.getenv("GITHUB_TOKEN")
    artifact_url=os.getenv("RUN_URL")
    max_findings_shown=int(os.getenv("MAX_FINDINGS_SHOWN","50"))
    data=sys.argv[1]
    trivy_data=load_trivy_results(data)
    severity_count=count_by_severity(trivy_data)
    findings=extract_findings(trivy_data)
    #print(findings)
    severity_rank = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    sorted_findings = sorted(findings, key=get_severity_rank)
    findings_to_show,remaining_count = findings_to_show(sorted_findings,max_findings_shown)
    formatted_report=report_formatter(findings_to_show,severity_count,remaining_count,artifact_url,cap=True)
    uncapped_formatted_report=report_formatter(sorted_findings,severity_count,0,artifact_url,cap=False)
    #print(uncapped_formatted_report)
    
    api=f"https://api.github.com/repos/{username}/{REPO}/issues/{ISSUE_NUMBER}/comments"
    headers = {"Authorization": f"Bearer {token}"}
    #print(sorted_findings)
    #print(formatted_report)
    response=post_comment(api,headers,formatted_report)
    
    print(response.status_code)
    print(response.text)
    print("Token length:", len(token) if token else "None")
    print("Token starts with:", token[:4] if token else "None")
    with open("full_report.md","w") as f:
        f.write(uncapped_formatted_report)
