import json
import sys


def load_trivy_results(json_path):
    with open(json_path, "r") as f:
        return json.load(f)


def count_by_severity(trivy_data):
    counts = {
            "CRITICAL" : 0,"HIGH" : 0,"MEDIUM" : 0,"LOW" : 0,"UNKNOWN" : 0
              }
    results = trivy_data.get("Results", [])
    #print(results)
    for result in results:
        #print(result)
        vulnerabilities = result.get("Vulnerabilities", [])
        #print(vulnerabilities)
        vuln_count = 0
        for vulnerability in vulnerabilities:
            #print(vulnerability)
            Severity = vulnerability.get("Severity" ,[])
            #print(Severity)
            if Severity in counts:
                counts[Severity] = counts[Severity] + 1


            vuln_count = vuln_count + 1
    return counts



def get_severity_rank(finding):
    severity_rank = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "UNKNOWN": 4}
    return severity_rank[finding["severity"]]


def extract_findings(trivy_data):
    findings = []
    results=trivy_data.get("Results", [])
    for result in results:
        vulnerabilities=result.get("Vulnerabilities", [])
        for vulnerability in vulnerabilities:
            findings.append({
                "id" : vulnerability.get("VulnerabilityID", "UNKNOWN"),
                "package_name" : vulnerability.get("PkgName", "UNKNOWN"),
                "installed_version" : vulnerability.get("InstalledVersion", "UNKNOWN"),
                "fixed_version" : vulnerability.get("FixedVersion", "UNKNOWN"),
                "severity" : vulnerability.get("Severity", "UNKNOWN"),
                "title" : vulnerability.get("Title", "UNKNOWN")
                })
    return findings
            #print("package name = ",package_name)
    

if __name__ == "__main__":
    json_path = sys.argv[1]
    print(json_path)
    data=load_trivy_results(json_path)
    #print(data)
    #print("\n\n findings:\n\n",extract_findings(data))
    #print("\n \n severitycount= ",count_by_severity(data))
    findings=extract_findings(data)
    severity_rank = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    sorted_findings = sorted(findings, key=get_severity_rank)
    print(sorted_findings)