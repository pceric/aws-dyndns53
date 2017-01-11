# dyndns53
My take on dynamic DNS using AWS Route 53.
Features support for both IPV4 A records and IPV6 AAAA records.
Works with Python 2.6+.

## Quick Start
Setup your AWS credentials. There are many ways to do this, see:
https://boto3.readthedocs.io/en/latest/guide/quickstart.html#configuration

Install Python requirements:
```
$ pip install -r requirements.txt
```

At the top of the script there are two variables you must change, `domain` and `subdomain`.
You must already have the hosted zone setup in your AWS account that matches `domain`.

Run the script `python dyndns53.py`. It works best when run on a cron every hour.
