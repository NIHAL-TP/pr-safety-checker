## Terraform Findings
### Summary 
- Total Resources Checked: 3
- Total Failed Checks: 9
### Detailed Findings
#### Resource: aws_vpc.mainvpc
- Failed Checks: 2
##### Failed Checks:
- Check CKV2_AWS_12 failed on path /terraform-sample/main.tf.Please Ensure the default security group of every VPC restricts all traffic
- Check CKV2_AWS_11 failed on path /terraform-sample/main.tf.Please Ensure VPC flow logging is enabled in all VPCs
#### Resource: aws_s3_bucket.s3
- Failed Checks: 7
##### Failed Checks:
- Check CKV2_AWS_61 failed on path /terraform-sample/main.tf.Please Ensure that an S3 bucket has a lifecycle configuration
- Check CKV2_AWS_6 failed on path /terraform-sample/main.tf.Please Ensure that S3 bucket has a Public Access block
- Check CKV2_AWS_62 failed on path /terraform-sample/main.tf.Please Ensure S3 buckets should have event notifications enabled
- Check CKV_AWS_145 failed on path /terraform-sample/main.tf.Please Ensure that S3 buckets are encrypted with KMS by default
- Check CKV_AWS_144 failed on path /terraform-sample/main.tf.Please Ensure that S3 bucket has cross-region replication enabled
- Check CKV_AWS_21 failed on path /terraform-sample/main.tf.Please Ensure all data stored in the S3 bucket have versioning enabled
- Check CKV_AWS_18 failed on path /terraform-sample/main.tf.Please Ensure the S3 bucket has access logging enabled




## Secrets Findings
### Summary 
 - Total secrets issues found: 1
### Detailed Findings
- Check " Base64 High Entropy String " with ID CKV_SECRET_6 failed on path /terraform-sample/provider.tf. 
  - Code Snippet: 
  ``` python
    secret_key = "my-**********"

  ```
  - Line Range: [4, 5]
