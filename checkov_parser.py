import sys
import json


def load_checkov_result(json_path):
    with open(json_path,"r") as f:
        data = json.load(f)
        return data


def extract_findings(checkov_result):
    failed_resources=set()
    summary = checkov_result["summary"]
    #print(f"{summary.get("resource_count")} resources checked {summary.get("failed")} issues found.")
    #passed_checks_data=checkov_result["results"]["passed_checks"]
    failed_checks_data=checkov_result["results"]["failed_checks"]
    findings = {}
    for failed_check in failed_checks_data:
        #print(failed_check) #{'check_id': 'CKV2_AWS_12', 'bc_check_id': 'BC_AWS_NETWORKING_4', 'check_name': 'Ensure the default security group of every VPC restricts all traffic', 'check_result': {'result': 'FAILED', 'entity': {'aws_vpc': {'mainvpc': {'__end_line__': 12, '__start_line__': 10, 'cidr_block': ['10.1.0.0/16'], '__address__': 'aws_vpc.mainvpc'}}}, 'evaluated_keys': ['egress/from_port', 'egress/to_port', 'egress/protocol', 'egress/cidr_blocks', 'ingress/from_port', 'resource_type', 'ingress/self', 'ingress/protocol', 'ingress/to_port']}, 'code_block': [[10, 'resource "aws_vpc" "mainvpc" {\n'], [11, '  cidr_block = "10.1.0.0/16"\n'], [12, '}\n']], 'file_path': '/main.tf', 'file_abs_path': '/home/nihal/pr-safety-checker/terraform-sample/main.tf', 'repo_file_path': '/terraform-sample/main.tf', 'file_line_range': [10, 12], 'resource': 'aws_vpc.mainvpc', 'evaluations': None, 'check_class': 'checkov.common.graph.checks_infra.base_check', 'fixed_definition': None, 'entity_tags': None, 'caller_file_path': None, 'caller_file_line_range': None, 'resource_address': None, 'severity': None, 'bc_category': None, 'benchmarks': None, 'description': None, 'short_description': None, 'vulnerability_details': None, '

        resource = failed_check.get("resource")
        check_id = failed_check.get("check_id")
        check_name = failed_check.get("check_name")
        resource_path = failed_check.get("repo_file_path")

        if "resources" not in findings:
            findings["resources"] = {}
        if "summary" not in findings:
            findings["summary"] = summary
        if resource not in findings["resources"]:
            findings["resources"][resource] = {"checks" : []}
        findings["resources"][resource]["checks"].append({
            "check_id": check_id,
            "check_name": check_name,
            "resource_path": resource_path
        })
    return findings
    

if __name__ == "__main__":
    json_path = sys.argv[1]
    checkov_result = load_checkov_result(json_path)
    findings = extract_findings(checkov_result)
    print(findings)
