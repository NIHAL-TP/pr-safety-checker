from parser import load_trivy_results,count_by_severity,extract_findings
import sys
import json


def report_formatter(findings,count):
    header_line=[]
    seperator_line=[]
    for i in findings:
        for j in i:    
            header_line.append(j)
            seperator_line.append("---|")
        print(header_line)
        print(seperator_line)

        break
    combined = header_line + seperator_line
    final_string = "\n".join(combined)
    print(final_string)

if __name__ == "__main__" :
    json_path=sys.argv[1]
    trivy_data = load_trivy_results(json_path)
    severity_count = count_by_severity(trivy_data)
    findings = extract_findings(trivy_data)
    """for i in findings:
        print("\n\n\n")
        for j in i:
            print(f"{j} : {i[j]}")"""
    report_formatter(findings,severity_count)