set -e

cd /smart-contracts

ganache-cli --port 7545 &

npm run build
npm run lint
npm run build-test

