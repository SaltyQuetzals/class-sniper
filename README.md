# Flare

A simple, easy-to-use command-line tool for monitoring seat status for specific sections at Texas A&M University, using Compass' newly-discovered (as of 2019) API.

## Prerequisites

1. A Gmail account that has granted less-secure apps access.


# Usage

The default usage (emails will be sent to `dummy@email.com`)
```sh
python3 main.py dummy@email.com dummypwd
```

But maybe you want to send emails to an address that's not yours? Emails in this case will be sent to `otherdummy@email.com`
```sh
python3 main.py dummy@email.com dummypwd -dest_email=otherdummy@email.com
```

