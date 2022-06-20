# System Design of a Public Facing REST API

## Requirements of a minimal viable product

The project is trying to build a MVP (minimal viable product) for prototyping and the initial stage of market testing of
a new product: a banking server provided by "NewBank" (a hypothetical bank). This project implements a bank (NewBank)
API to list debit card transactions.

### API

- Allow new users to sign up.
- Allow users to get access token (sign in).
- Allow users to renew access token from refresh token.
- List the debit card transaction list on the Unit Sandbox. There are currently 7 transactions. See the bottom of the
  README.md.
- Allow users to sign out.

Enhancement needed for production:

- Add multi-factor authentication for new users.

### Unit Sandbox Setup

The debit card transactions are created from batches in directory bank-api-app/unit.

- unit_setup_env.sh: Passing the read token and write token by environment variables.
- unit_create_individual_virtual_debit_card.sh: Creating a new individual virtual debit card, which is active after
  creation.
- unit_create_card_transaction.sh: Creating debit / credit transactions.
- unit_list_transaction.sh: Listing the debit card transactions.

### Security

The API authentication and authorization is done by JWT.

### https

Server / port / endpoint

The port is currently on 80.

Enhancement needed for production:

- Get an SSL certificate from Let's Encrypt or another certificate provider.
- Configure Apache to use the SSL certificate.

### Logging

The logs are written to console.

Enhancement needed for production:

- Use a production server such as ELK.

### Config

The configuration values and secrets are provided in env.sh files and bank-api-app/bank_api/app/website/config.py

Enhancement needed for production:

- Pass configuration values and secrets through environment variables.
- Store the secrets in a secret vault instead of plain text.

### Database

The database is a local MySQL server in a Docker container.

Enhancement needed for production:

- Use a production database such as AWS RDS.
- Save and persist the access token / refresh token in a database.

### Testing

The tests are in bank-api-app/bank_api/app/website/tests/test_bank_api.py

The tests cover the following features.

- Allow new users to sign up.
- Allow users to get access token (sign in).
- Allow users to renew access token from refresh token.
- List the debit card transaction list on the Unit Sandabox.

### Single server deployment

The setup is for a MVP with essential features. The implementation is done by EC2 + Docker + Apache + Flask.

- The Flask server runs behind Apache for better performance.

Enhancement needed for production:

- Run the API server behind a load balancer on EKS for scalability.

## How to Deploy and Run the Application?

### Step 1: Change Server IPs.

The MySQL server and API Server run in Docker containers. The IP needs to be accessible between MySQL Server, API Server
and the client.

- Inside the directory bank-api-app, search and replace "MYSERVERIP" to IP of the local computer.

### Step 2: Start MySQL Server

The MySQL Server runs in a Docker container on the local computer. Step 2 will take ~3 minutes for the MySQL server to
start. The data is persisted at /srv/var/lib/mysql. Change it if somewhere else is better.

- Go to directory bank-api-app/database
- Run the command "./database_run.sh"

The command will build a Docker image and then run it.

### Step 3: Prepare MySQL Server

Step 3 creates the database "newbank".

- Go to directory bank-api-app/bank-api
- Run the command "./prepare_mysql_server.sh"

The command will build a Docker image and then run it.

### Step 4: Start the Bank API Server

The REST API Server runs in a Docker container on the local computer.

- Go to directory bank-api-app/bank-api
- Run the command "./server_run.sh"

The command will build / rebuild a Docker image and then run it.

### Step 5: Run the client.

The REST API Server runs in a Docker container on the local computer.

- Go to directory bank-api-app/client
- Run the command "./client_run.sh"

The command will build a Docker image and then run it.

```
Debit Transaction List:
================================================================================
Transaction: 1
================================================================================
{'attributes': {'amount': 20,
                'balance': 11080,
                'cardLast4Digits': '9990',
                'createdAt': '2022-03-20T03:26:09.422Z',
                'direction': 'Debit',
                'interchange': None,
                'internationalServiceFee': None,
                'merchant': {'category': '',
                             'location': 'Cupertino, CA',
                             'name': 'Apple Inc.',
                             'type': 1000},
                'paymentMethod': 'Swipe',
                'recurring': False,
                'summary': 'summary text  |  **9990'},
 'id': '914973',
 'relationships': {'account': {'data': {'id': '373055', 'type': 'account'}},
                   'card': {'data': {'id': '162817', 'type': 'card'}},
                   'customer': {'data': {'id': '260844', 'type': 'customer'}},
                   'customers': {'data': [{'id': '260844',
                                           'type': 'customer'}]},
                   'org': {'data': {'id': '1168', 'type': 'org'}}},
 'type': 'cardTransaction'}
================================================================================
Transaction: 2
================================================================================
{'attributes': {'amount': 200,
                'balance': 11280,
                'cardLast4Digits': '9990',
                'createdAt': '2022-03-20T03:26:34.889Z',
                'direction': 'Credit',
                'interchange': None,
                'internationalServiceFee': None,
                'merchant': {'category': '',
                             'location': 'Cupertino, CA',
                             'name': 'Apple Inc.',
                             'type': 1000},
                'paymentMethod': 'Swipe',
                'recurring': False,
                'summary': 'summary text  |  **9990'},
 'id': '914974',
 'relationships': {'account': {'data': {'id': '373055', 'type': 'account'}},
                   'card': {'data': {'id': '162817', 'type': 'card'}},
                   'customer': {'data': {'id': '260844', 'type': 'customer'}},
                   'customers': {'data': [{'id': '260844',
                                           'type': 'customer'}]},
                   'org': {'data': {'id': '1168', 'type': 'org'}}},
 'type': 'cardTransaction'}
================================================================================
Transaction: 3
================================================================================
{'attributes': {'amount': 20000,
                'balance': 31280,
                'cardLast4Digits': '9990',
                'createdAt': '2022-03-20T03:26:56.900Z',
                'direction': 'Credit',
                'interchange': None,
                'internationalServiceFee': None,
                'merchant': {'category': '',
                             'location': 'Cupertino, CA',
                             'name': 'Apple Inc.',
                             'type': 1000},
                'paymentMethod': 'Swipe',
                'recurring': False,
                'summary': 'summary text  |  **9990'},
 'id': '914975',
 'relationships': {'account': {'data': {'id': '373055', 'type': 'account'}},
                   'card': {'data': {'id': '162817', 'type': 'card'}},
                   'customer': {'data': {'id': '260844', 'type': 'customer'}},
                   'customers': {'data': [{'id': '260844',
                                           'type': 'customer'}]},
                   'org': {'data': {'id': '1168', 'type': 'org'}}},
 'type': 'cardTransaction'}
================================================================================
Transaction: 4
================================================================================
{'attributes': {'amount': 3000,
                'balance': 28280,
                'cardLast4Digits': '9990',
                'createdAt': '2022-03-20T03:33:57.741Z',
                'direction': 'Debit',
                'interchange': None,
                'internationalServiceFee': None,
                'merchant': {'category': '',
                             'location': 'Redmond, WA',
                             'name': 'Microsoft',
                             'type': 1000},
                'paymentMethod': 'Swipe',
                'recurring': False,
                'summary': 'Online scheduled payment to CRD 4950 Confirmation '
                           '#2060795209  |  **9990'},
 'id': '914976',
 'relationships': {'account': {'data': {'id': '373055', 'type': 'account'}},
                   'card': {'data': {'id': '162817', 'type': 'card'}},
                   'customer': {'data': {'id': '260844', 'type': 'customer'}},
                   'customers': {'data': [{'id': '260844',
                                           'type': 'customer'}]},
                   'org': {'data': {'id': '1168', 'type': 'org'}}},
 'type': 'cardTransaction'}
================================================================================
Transaction: 5
================================================================================
{'attributes': {'amount': 6000,
                'balance': 22280,
                'cardLast4Digits': '9990',
                'createdAt': '2022-03-20T03:35:55.556Z',
                'direction': 'Debit',
                'interchange': None,
                'internationalServiceFee': None,
                'merchant': {'category': '',
                             'location': 'Redmond, WA',
                             'name': 'Bank of America',
                             'type': 1000},
                'paymentMethod': 'Swipe',
                'recurring': False,
                'summary': 'BANK OF AMERICA CREDIT CARD Bill Payment  |  '
                           '**9990'},
 'id': '914977',
 'relationships': {'account': {'data': {'id': '373055', 'type': 'account'}},
                   'card': {'data': {'id': '162817', 'type': 'card'}},
                   'customer': {'data': {'id': '260844', 'type': 'customer'}},
                   'customers': {'data': [{'id': '260844',
                                           'type': 'customer'}]},
                   'org': {'data': {'id': '1168', 'type': 'org'}}},
 'type': 'cardTransaction'}
================================================================================
Transaction: 6
================================================================================
{'attributes': {'amount': 4769,
                'balance': 17511,
                'cardLast4Digits': '9990',
                'createdAt': '2022-03-20T03:38:26.543Z',
                'direction': 'Debit',
                'interchange': None,
                'internationalServiceFee': None,
                'merchant': {'category': '',
                             'location': 'PALMDALE CA',
                             'name': 'Walmart',
                             'type': 1000},
                'paymentMethod': 'Swipe',
                'recurring': False,
                'summary': 'WAL-MART #1660 10/23 PURCHASE PALMDALE CA  |  '
                           '**9990'},
 'id': '914978',
 'relationships': {'account': {'data': {'id': '373055', 'type': 'account'}},
                   'card': {'data': {'id': '162817', 'type': 'card'}},
                   'customer': {'data': {'id': '260844', 'type': 'customer'}},
                   'customers': {'data': [{'id': '260844',
                                           'type': 'customer'}]},
                   'org': {'data': {'id': '1168', 'type': 'org'}}},
 'type': 'cardTransaction'}
================================================================================
Transaction: 7
================================================================================
{'attributes': {'amount': 1824,
                'balance': 15687,
                'cardLast4Digits': '9990',
                'createdAt': '2022-03-20T03:40:58.914Z',
                'direction': 'Debit',
                'interchange': None,
                'internationalServiceFee': None,
                'merchant': {'category': '',
                             'location': 'Cupertino, CA',
                             'name': 'Chase',
                             'type': 1000},
                'paymentMethod': 'Swipe',
                'recurring': False,
                'summary': 'Online Banking payment to CRD 4950 Confirmation# '
                           '0279381921  |  **9990'},
 'id': '914979',
 'relationships': {'account': {'data': {'id': '373055', 'type': 'account'}},
                   'card': {'data': {'id': '162817', 'type': 'card'}},
                   'customer': {'data': {'id': '260844', 'type': 'customer'}},
                   'customers': {'data': [{'id': '260844',
                                           'type': 'customer'}]},
                   'org': {'data': {'id': '1168', 'type': 'org'}}},
 'type': 'cardTransaction'}

```

## Caveats
- This is a four-hour homework project. Do not use this in production.
- All user and account information are emptied out. You will need to set them up properly before testing.