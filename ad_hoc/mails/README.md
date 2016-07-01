# mail-parser

## Overview

Parse emails from a file or string, and store generated schema.

## Extraction of email file

Extract structural information from an email file or an email message string.

### Notes

1. If mail is multipart, parser will call itself recursively to extract information.

2. Type field is not recognizable for mongoDB, they are currently transformed into str.


## Storage of schema

Use mongo to store the extracted schema. For development use, we use a mongo docker image, and port 27017 as default port.
But you can define your personalized mongo server by exporting environmental variable:

`__DB_ADDR__ (address of your server including port)`

`__DB_USER__ (if you wish to make your data safer)`

`__DB_PASS__ (if you wish to make your data safer)`

## Docker compose for mongo

For easier use, default mongoDB are settled in docker-compose file.

General use:
```
docker-compose up -d

python mail-parser/mail-parser.py --filename='data/example.eml'
```

### Notes

1. mail-parser.py accept following options:
    -conf: with `__DB_ADDR__`, `__DB_USER__`, etc.

    -filename: the email file to parse

    -mail-str: the email string to parse

    (use either filename or mail_str, if mail_str exists, it will be parsed, otherwise use email file)