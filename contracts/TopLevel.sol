pragma solidity ^0.4.0;

import "./Article.sol";

contract TopLevel {

    mapping (bytes32 => address) articles;

    function TopLevel() public {

    }

    function createArticle(bytes32 titleHash, bytes32 ID) public {
        require(articles[titleHash] == 0); // TODO - handle hash collision

        articles[titleHash] = new Article(ID);
    }

    function getArticle(bytes32 titleHash) public view returns(address) {
        return articles[titleHash];
    }

}
