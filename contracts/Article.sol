pragma solidity ^0.4.0;

contract Article {

    struct Commit {
        // TODO - what type should we use for ipfs hash?
        // https://ethereum.stackexchange.com/questions/17094/how-to-store-ipfs-hash-using-bytes?noredirect=1&lq=1
        bytes32 ID; // TODO - should we use IPNS?
        address Author;
        uint timestamp;
    }

    struct Request {
        bytes32 ID;
        address Author;
        uint votes;
    }

    // changes made to article
    Commit[] public commits;

    // list of all active modify requests
    Request[] public modifyRequests; // TODO - create separate contract to store modify requests,
                                     // after modify request if merged/rejected this contract can be destructed
                                     // and funds for storage will be refunded (!need to confirm that!)
                                     // TODO - another option is to save requests after merging one of them
                                     // for another turn (voting starts again from 0)

    // number of active requests
    uint public nModifyRequests = 0;

    uint public constant RequiredVotes = 10;

    // event emitted when article is modified
    event ArticleUpdated(bytes32 newId);

    function Article(address author, bytes32 Id) public {
        commits.push(Commit({
            ID: Id,
            Author: author,
            timestamp: now
        }));
    }

    function getArticleID() public view returns(bytes32){
        return commits[commits.length - 1].ID;
    }

    function nModifications() public view returns(uint) {
        return commits.length;
    }

    function update(bytes32 Id, address author) private {
        commits.push(Commit({
            ID: Id,
            Author: author,
            timestamp: now
        }));

        // clear requests
        nModifyRequests = 0;

        emit ArticleUpdated(Id);
    }

    function vote(uint requestNumber) public {
        require(requestNumber < nModifyRequests);

        modifyRequests[requestNumber].votes++;

        Request memory request = modifyRequests[requestNumber];
        if (request.votes >= RequiredVotes) {
            update(request.ID, request.Author);  // TODO - move to separate function? (called by author?) -
                                                 // so that voter would not need to pay for article update
        }
    }

    function modify(bytes32 newId) public {
        Request memory request = Request({
            ID: newId,
            Author: msg.sender,
            votes: 0
        });

        // if table has no space to store more requests we extend it, otherwise
        // we reuse space
        if (modifyRequests.length == nModifyRequests) {
            modifyRequests.push(request);
        } else {
            modifyRequests[nModifyRequests] = request;
        }

        nModifyRequests++;
    }
}
