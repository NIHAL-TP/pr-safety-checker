import requests
import sys
from trivy_parser import load_trivy_results, extract_findings, count_by_severity
from trivy_report_formatter import report_formatter, get_severity_rank, findings_to_show
from checkov_parser import load_checkov_result, extract_findings as extract_checkov_findings
from checkov_report_formatter import checkov_report_formatter
import os
from dotenv import load_dotenv
load_dotenv()


def post_comment(api,headers,trivy_comment):
    #print("api:",api)
    response=requests.post(api,headers = headers,json={"body":trivy_comment})
    return response


if __name__ == "__main__":
    trivy_json_path=sys.argv[1]

    REPO = "pr-safety-checker"
    ISSUE_NUMBER = "1"
    token = os.getenv("GITHUB_TOKEN")
    username = os.getenv("GITHUB_USER")
    artifact_url=os.getenv("RUN_URL")
    max_findings_shown=int(os.getenv("MAX_FINDINGS_SHOWN","50"))
    api=f"https://api.github.com/repos/{username}/{REPO}/issues/{ISSUE_NUMBER}/comments"
    headers = {"Authorization": f"Bearer {token}"}
    trivy_data=load_trivy_results(trivy_json_path)
    trivy_findings=extract_findings(trivy_data)
    severity_count=count_by_severity(trivy_data)
    severity_rank = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    sorted_findings = sorted(trivy_findings, key=get_severity_rank)
    findings_to_show,remaining_count = findings_to_show(sorted_findings,max_findings_shown)
    formatted_trivy_report=report_formatter(findings_to_show,severity_count,remaining_count,artifact_url,cap=True)
    uncapped_formatted_report=report_formatter(sorted_findings,severity_count,0,artifact_url,cap=False)

    checkov_json_path=sys.argv[2]
    checkov_result = load_checkov_result(checkov_json_path)
    checkov_findings = extract_checkov_findings(checkov_result)
    checkov_comment = checkov_report_formatter(checkov_findings)
    comment = formatted_trivy_report + "\n\n\n" + checkov_comment
    
    response = post_comment(api,headers,comment)
    print("Response status code:", response.status_code)


