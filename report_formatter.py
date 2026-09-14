from parser import load_trivy_results,count_by_severity,extract_findings
import sys
import json
#is

def get_severity_rank(finding):
    severity_rank = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 4, "UNKNOWN": 3}
    return severity_rank[finding["severity"]]


def findings_to_show(findings,MAX_FINDINGS_SHOWN):
    findings_to_show = findings[:MAX_FINDINGS_SHOWN]
    remaining_count = len(findings) - len(findings_to_show)
    return findings_to_show,remaining_count



def report_formatter(findings,count,remaining_count,artifact_url,cap=True):
    header_line=[]
    seperator_line=[]
    content=[]
    table=[]
    char = "|"
    for line in findings:
        #print(line)
        for j in line:    
            header_line.append(j)
            seperator_line.append("---")
        combined_header = char + " | ".join(header_line) + char
        combined_seperator = char +  " | ".join(seperator_line) + char
        #print(header_line)
        #print(seperator_line)
        break
    #print(combined_header)
    #print(combined_seperator)
    for line in findings:
        content_line=[]
        for j in line:
            content_line.append(line[j])
        combined_content_line = char + " | ".join(content_line)+ char
        content.append(combined_content_line)
    combined_content = "\n".join(content)
    #print(combined_content)
    table.append(combined_header)
    table.append(combined_seperator)
    table.append(combined_content)
    table = "\n".join(table)
    if cap:
        table = f"**Summary:** {count['CRITICAL']} CRITICAL, {count['HIGH']} HIGH, {count['MEDIUM']} MEDIUM, {count['LOW']} LOW, {count['UNKNOWN']} UNKNOWN severity issues found.\n Top 50 issues shown below,check artifacts at {artifact_url} for further details" + "\n" + table
    else:
        table = table
    print("length of table is ",len(table))
    return table

    

if __name__ == "__main__" :
    json_path=sys.argv[1]
    max_findings_shown=10
    trivy_data = load_trivy_results(json_path)
    severity_count = count_by_severity(trivy_data)
    findings = extract_findings(trivy_data)
    severity_rank = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    sorted_findings = sorted(findings, key=get_severity_rank)
    print(sorted_findings)
    findings_to_show,remaining_count=findings_to_show(sorted_findings,max_findings_shown)
    #print(findings)
    print("remaining count:",remaining_count)
    print("findings in markdown \n",report_formatter(findings_to_show,severity_count,remaining_count))
