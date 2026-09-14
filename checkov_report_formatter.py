from checkov_parser import extract_findings, load_checkov_result
import sys
def checkov_report_formatter(findings):
    report = ""
    report += f"## Checkov Findings\n"
    report += f"### Summary \n"
    summary = findings.get("summary", {})
    report += f"- Total Resources Checked: {summary.get("resource_count", 0)}\n"
    report += f"- Total Failed Checks: {summary.get("failed", 0)}\n"
    report += f"### Detailed Findings\n"
    for resource in findings["resources"]:
        print(findings["resources"][resource]["checks"][0])

    return(report)


if __name__ == "__main__":
    json_path=sys.argv[1]
    checkov_result = load_checkov_result(json_path)
    findings = extract_findings(checkov_result)
    report = checkov_report_formatter(findings)
    #print(report)
