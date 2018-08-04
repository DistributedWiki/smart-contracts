pragma solidity ^0.4.0;

contract Article {

    struct Commit {
        // TODO - what type should we use for ipfs hash?
        // https://ethereum.stackexchange.com/questions/17094/how-to-store-ipfs-hash-using-bytes?noredirect=1&lq=1
        bytes32 ID; // TODO - should we use IPNS?
        address Author;
        uint timestamp;
    }

    // changes made to article
    Commit[] public commits;

    // event emitted when article is modified
    event ArticleUpdated(bytes32 newId);

    function Article(bytes32 Id) public {
        commits.push(Commit({
            ID: Id,
            Author: msg.sender,
            timestamp: block.timestamp
        }));
    }

    // returns ID of latest version of article
    function getArticleID() public view returns(bytes32){
        return commits[commits.length - 1].ID;
    }

    // returns number of modifications made to article
    function nModifications() public view returns(uint) {
        return commits.length;
    }

    function update(bytes32 Id) public {
        commits.push(Commit({
            ID: Id,
            Author: msg.sender,
            timestamp: block.timestamp // This is inaccurate (this value is set by miner)
        }));

        emit ArticleUpdated(Id);
    }
}
