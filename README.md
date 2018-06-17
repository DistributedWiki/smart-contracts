## Distributed Wikipedia

[![Build Status](https://travis-ci.org/chorig9/blockchain.svg?branch=master)](https://travis-ci.org/chorig9/blockchain)

### Requirements

See package.json

Currently only Linux is supported

### How to run

* set-up testrpc node (e.g. [Ganache](https://github.com/trufflesuite/ganache))

* To compile, migrate and run tests run:
```Bash
npm run build
```

* To run linter:
```Bash
npm run lint
```

* To fix issues reported by linter:
```Bash
npm run lint:fix
```

### Running with docker

Docker image ready for smart contracts deployment is provided.
To use, run:

```
cd utils
docker build -f Dockerfile.contracts -t contracts .
docker run -p 7545:7545 contracts /bin/sh ./run.sh
```
