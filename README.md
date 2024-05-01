# MessagingService

## Getting started

Follow these steps to prepare and run the server. Make sure that you are in the root of the project, where <code>manage.py</code> is located.

1. <code>pip3 install -r requirements.txt</code>
2. <code>python3 manage.py makemigrations messagingService</code>
4. <code>python manage.py migrate</code>
5. <code>python3 manage.py runserver</code>

## Run the requests:

### Users
In order to be able to use the messaging service, you first need to create at least one user. You can create new users with

```
curl -H 'Content-Type: application/json' \
      -d '{ "name":"username"}' \
      -X POST \
      localhost:8000/users/
```
      
There is also an endpoint for viewing all created users:

```
curl localhost:8000/users/
```

Users are identified by their usernames, which need to be unique.
### Messages

#### Send a message

```
curl -H 'Content-Type: application/json' \
      -d '{"content":"Hello world!", "sender": "username"}' \
      -X POST \
      localhost:8000/users/username/messages/
```

#### Get new messages for a user

```
curl localhost:8000/users/username/messages/
```

#### Get messages within a specific timeframe for a user

The timeframes are set with query string parameters. Ex:

```
curl "localhost:8000/users/username/messages/?startdate=2024-05-01T18:10:23.742215Z&enddate=2024-05-01T18:10:38.357211Z"
```

or 

```
curl "localhost:8000/users/username/messages/?startdate=2024-05-01T18:10:23.742215Z"
```

#### Remove messages

Messages can be removed by their receiver username or by the message id.

This command removes all messages to the user with username *username*
```
curl -X Delete localhost:8000/users/username/messages/
```

or 

```
curl -X Delete http://127.0.0.1:8000/messages/1
```

