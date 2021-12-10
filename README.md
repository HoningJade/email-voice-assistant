# email-voice-assistant
Awesome web voice assistant for email. Course project of EECS 498-006 FA21@umich

<img width="777" alt="image" src="https://user-images.githubusercontent.com/49838100/144513923-e075a8e6-ab95-4502-b086-1761dc58ad24.png">

# Run
```
$ python bin/run_all.py
$ python bin/run_all.py --debug
```

## Backend
### Set up backend module
Recommend python3.7+
```
$ cd backend
$ pip install -e .
```
### Run backend module
```
$ ./bin/run_backend    # debug off
$ ./bin/debug_backend  # debug on
```
### HTTP requests
#### Execute command (method: `GET` with _json_)
- Mark as `read`/`unread`
- ...

```
{
   "id": 1,
   "command": "unread",
   "args":{}
}

```
---

## NLP
### Set up NLP module
Recommend python3.7+
```
$ cd nlp
$ pip install -e .
```
### Run backend module
```
$ ./bin/run_nlp    # debug off
$ ./bin/debug_nlp  # debug on
```
---

## Frontend
### Set up frontend dependencies
For local test, require `node>=15.0.0` (we recommend 15.0.1) and `npm>=5.6`.

#### node
To install `node` with the latest version, we need `nvm` (Node Version Manager) on Ubuntu.
```
$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
# restart bash
```
You can verify that `nvm` is installed by calling
```
$ nvm --version
```
Then, to install node, you can call
```
$ nvm install 15.0.1
```
To verify version of `node`, you can call
```
$ node -v
```

#### npm and yarn
Then we call install `npm` by
```
$ sudo apt install npm
```
Then we set up `yarn` using `npm`
```
$ cd frontend
$ npm install --global yarn
```

#### Build the app
After that, we can build the app
```
$ cd frontend
$ yarn install
```
#### Run frontend module
```
$ yarn start
```
