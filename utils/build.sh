#!/usr/bin/env bash

# Exit on error
set -e 

truffle compile
truffle migrate --reset
truffle test
