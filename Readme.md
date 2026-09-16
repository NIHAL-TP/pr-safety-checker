# PR Safety Checker

When developers update code, they usually test for one thing: does it work. Once the functionality is correct, they open a pull request to merge it into main. Security isn't usually part of that check , it's easy to miss a public S3 bucket or an outdated base image when the app itself runs fine.

This project catches that gap. When a pull request is opened, a GitHub Actions pipeline automatically builds the app's Docker image and scans it with Trivy for vulnerabilities, checks the Terraform config with Checkov for misconfigurations and exposed secrets, and posts the results as a comment directly on the PR , before anything gets merged.

## How it works

When a developer opens a pull request, a GitHub Actions pipeline kicks off automatically. It builds the Docker image and scans it with Trivy, once for image vulnerabilities and once for Dockerfile misconfigurations, and Trivy writes its results out as JSON. At the same time, Checkov scans the Terraform files for misconfigurations and hardcoded secrets, and writes its own JSON output.

A Python program then takes both of those JSON files, parses them, and builds one combined report. Trivy's findings come with a severity rating, so those get ranked and sorted by how serious they are critical and high first. Checkov's free version doesn't provide severity for its findings, so those are grouped by resource instead, showing exactly which part of the infrastructure has issues.

GitHub comments have a character limit, and a single scan can easily return more findings than that limit allows; one test run came back with over 1,600 vulnerabilities. So the comment only shows the top 50 issues, and the full, uncapped report is uploaded as a workflow artifact anyone on the PR can download.

## Why I built it this way

Trivy and Checkov both have built-in output formats, but using them directly doesn't give much control over what actually gets shown. Writing a custom Python layer meant I could filter, rank, and format the results exactly the way I wanted, instead of being stuck with whatever the tool decides to print.

For Terraform specifically, I went with Checkov over the alternatives. It doesn't just check a resource in isolation , it understands relationships between resources, so it can catch things a simple rule-by-rule scan would miss. It's also still actively maintained, which matters for a tool you're relying on to catch real security issues.

One decision I want to call out: some Trivy findings come back with no severity at all, just UNKNOWN. My first instinct was to rank those dead last, below LOW, so they wouldn't clutter the top of the report. But that didn't sit right,an unclassified finding isn't the same as a confirmed-safe one, and burying it at the bottom meant it could get cut off entirely once the report is capped at 50 issues. So I ranked UNKNOWN just above LOW instead: visible in the report, but not treated as more urgent than it's actually known to be.

## Tech stack 
- Docker - the sample app is built into an image, which is what actually gets scanned
- GitHub Actions - runs the whole pipeline automatically on every pull request
- Trivy - scans the Docker image for known vulnerabilities and the Dockerfile for misconfigurations
- Checkov - scans Terraform files for misconfigurations and hardcoded secrets
- Python - parses the JSON output from both scanners, ranks and formats the findings, and posts the final report as a PR comment via the GitHub API

## Setup and usage
### Just using the tool

Fork the repo, create a new branch, and replace the contents of sample-app with your own Dockerfile and application. Add your Terraform files the same way. Open a pull request to the main branch, and the pipeline runs automatically . you'll see the results as a comment on the PR. Every time you push a new commit to that branch, the pipeline runs again, so you don't need to merge to see updated results.

You don't need to set up a .env file or a token for this. GITHUB_TOKEN is provided automatically by GitHub Actions on every run, and the username and PR number are pulled directly from the pull request itself.

### Running the scripts locally

If you want to run the Python scripts on your own machine outside of Actions for testing or development , you'll need a .env file with:

```
GITHUB_TOKEN=<github-token>
GITHUB_USER=<github-username>
ISSUE_NUMBER=<pr-number>
MAX_FINDINGS_SHOWN=50
```
GITHUB_TOKEN here needs to be a personal access token you generate yourself, since the automatic one only exists inside an Actions run. ISSUE_NUMBER should be a real PR number on your repo, since the script posts a comment to it.

## Limitations
This is static analysis only. It checks what your code describes, not what's actually running in a real cloud account;it won't catch infrastructure drift, where someone's made manual changes outside of Terraform.
Checkov's free version doesn't return severity ratings, so Terraform findings are grouped by resource instead of ranked by how serious they are, unlike the Docker findings.
The checks are general, industry-standard best practices, not your organization's own policies. Something your team has deliberately decided is acceptable will still get flagged every time, with no built-in way to mark it as a reviewed exception.
The Docker scan depends on the image actually building successfully. If the Dockerfile is broken, the whole check fails before any scanning happens,which is intentional, but worth knowing.