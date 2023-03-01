# gcp-auth

Runs `gcloud auth` to authenticate at the GCP.

## Requirements

- gcloud CLI

## Variables

| Name                     | Mandatory | Description                                                |
| ------------------------ | --------- | ---------------------------------------------------------- |
| gcp_project              | yes       | the gcp project name to use for the invocation             |
| gcp_service_account_file | yes       | the path to the `serviceaccount.json` to authenticate with |
