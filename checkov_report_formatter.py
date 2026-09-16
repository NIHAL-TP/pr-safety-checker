from checkov_parser import extract_findings, load_checkov_result
import sys
def checkov_report_formatter(findings):
    #print(findings)#{'terraform_findings': {'resources': {'aws_vpc.mainvpc': {'checks': [{'check_id': 'CKV2_AWS_12', 'check_name': 'Ensure the default security group of every VPC restricts all traffic', 'resource_path': '/terraform-sample/main.tf'}, {'check_id': 'CKV2_AWS_11', 'check_name': 'Ensure VPC flow logging is enabled in all VPCs', 'resource_path': '/terraform-sample/main.tf'}]}, 'aws_s3_bucket.s3': {'checks': [{'check_id': 'CKV2_AWS_61', 'check_name': 'Ensure that an S3 bucket has a lifecycle configuration', 'resource_path': '/terraform-sample/main.tf'}, {'check_id': 'CKV2_AWS_6', 'check_name': 'Ensure that S3 bucket has a Public Access block', 'resource_path': '/terraform-sample/main.tf'}, {'check_id': 'CKV2_AWS_62', 'check_name': 'Ensure S3 buckets should have event notifications enabled', 'resource_path': '/terraform-sample/main.tf'}, {'check_id': 'CKV_AWS_145', 'check_name': 'Ensure that S3 buckets are encrypted with KMS by default', 'resource_path': '/terraform-sample/main.tf'}, {'check_id': 'CKV_AWS_144', 'check_name': 'Ensure that S3 bucket has cross-region replication enabled', 'resource_path': '/terraform-sample/main.tf'}, {'check_id': 'CKV_AWS_21', 'check_name': 'Ensure all data stored in the S3 bucket have versioning enabled', 'resource_path': '/terraform-sample/main.tf'}, {'check_id': 'CKV_AWS_18', 'check_name': 'Ensure the S3 bucket has access logging enabled', 'resource_path': '/terraform-sample/main.tf'}]}}, 'terraform_summary': {'passed': 5, 'failed': 9, 'skipped': 0, 'parsing_errors': 0, 'resource_count': 3, 'checkov_version': '3.3.17'}}, 'secret_findings': {'secrets_summary': {'passed': 0, 'failed': 1, 'skipped': 0, 'parsing_errors': 0, 'resource_count': 1, 'checkov_version': '3.3.17'}, '/terraform-sample/provider.tf': {'checks': [{'check_id': 'CKV_SECRET_6', 'check_name': 'Base64 High Entropy String', 'code_snippet': '    secret_key = "my-**********"\n', 'line_range': [4, 5]}]}}}
    terraform_report = ""
    check_id=set()
    terraform_report += f"## Terraform Findings\n"
    terraform_report += f"### Summary \n"
    terraform_summary = findings["terraform_findings"].get("terraform_summary", {})
    #print(terraform_summary)
    terraform_report += f"- Total Resources Checked: {terraform_summary.get("resource_count", 0)}\n"
    terraform_report += f"- Total Failed Checks: {terraform_summary.get("failed", 0)}\n"
    terraform_report += f"### Detailed Findings\n"
    for resource in findings["terraform_findings"]["resources"]:
        terraform_report += f"#### Resource: {resource}\n"
        terraform_report += f"- Failed Checks: {len(findings["terraform_findings"]["resources"][resource]["checks"])}\n"
        terraform_report += f"##### Failed Checks:\n"
        for check in findings["terraform_findings"]["resources"][resource]["checks"]:
            """if check["check_id"] not in check_id:
                check_id.add(check["check_id"])"""
            terraform_report += f"- Check {check['check_id']} failed on path {check['resource_path']}.Please {check['check_name']}\n"
            
            #print(f"Resource: {resource}")
            """print(findings["terraform_findings"]["resources"][resource]["checks"])
            
            for check in findings["terraform_findings"]["resources"][resource]["checks"]:
                print(f"failed Check: {check}")"""


    secrets_report = ""
    secrets_report += f"## Secrets Findings\n"
    secrets_report += f"### Summary \n"
    secrets_summary = findings["secret_findings"].get("secrets_summary", {})
    #print(secrets_summary)
    secrets_report += f" - Total secrets issues found: {secrets_summary.get("failed", 0)}\n"
    secrets_report += f"### Detailed Findings\n"
    #print(findings["secret_findings"])
    for secret_issue in findings["secret_findings"].get("secret_issues")["checks"]:
        secrets_report += f"- Check \" {secret_issue['check_name']} \" with ID {secret_issue['check_id']} failed on path {secret_issue['file_path']}. \n"
        secrets_report += f"  - Code Snippet: \n"
        secrets_report += f"  ``` python\n"
        secrets_report += f"{secret_issue['code_snippet']}\n"
        secrets_report += f"  ```\n"
        secrets_report += f"  - Line Range: {secret_issue['line_range']}\n"
    report = terraform_report + "\n\n\n\n" + secrets_report
    with open("checkov_report.md", "w") as f:
        f.write(report)
    return(report)


if __name__ == "__main__":
    json_path=sys.argv[1]
    checkov_result = load_checkov_result(json_path)
    findings = extract_findings(checkov_result)
    report = checkov_report_formatter(findings)
    print(report)
