## IPFS as a decentralized storage

### Requirements
* ipfs(v0.4.14)

### Installation
```bash
wget https://dist.ipfs.io/go-ipfs/v0.4.14/go-ipfs_v0.4.14_linux-amd64.tar.gz
tar xvzf go-ipfs_v0.4.14_linux-amd64.tar.gz
cd go-ipfs
sudo ./install.sh
```

Confirm installation looking at version of ipfs. (It should be v0.4.14.):
```bash
ipfs version
```

### Initialization
```bash
ipfs init # generates local-repo and rsa keypair
ipfs daemon # runs ipfs daemon and connects to network
```

### Cheatsheet

#### Check your peers
```bash
ipfs swarm peers
```
Output pattern: `<transport address config>/ipfs/<hash-of-public-key>`

#### Save object from network to file
```bash
ipfs cat /ipfs/<hash-of-public-key>/filename > output_file
```

#### Add file to network
```bash
ipfs add <file_path>
```

#### Test access to file through public gateway
```bash
curl https://ipfs.io/ipfs/<hash-of-public-key>
```
