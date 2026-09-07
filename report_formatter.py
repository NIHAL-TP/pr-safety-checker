from parser import load_trivy_results,count_by_severity,extract_findings
import sys
import json


def report_formatter(findings,count):
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
    table = f"**Summary:** {count['HIGH']} HIGH, {count['MEDIUM']} MEDIUM issues found" + "\n" + table
    return table

    

if __name__ == "__main__" :
    json_path=sys.argv[1]
    trivy_data = load_trivy_results(json_path)
    severity_count = count_by_severity(trivy_data)
    findings = extract_findings(trivy_data)
    """for i in findings:
        print("\n\n\n")
        for j in i:
            print(f"{j} : {i[j]}")"""
    print("findings in markdown \n",report_formatter(findings,severity_count))