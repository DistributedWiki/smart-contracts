pragma solidity ^0.4.0;

import "./Article.sol";

contract TopLevel {

    mapping (bytes32 => address) articles;
    bytes32[] public titlesList;

    function TopLevel() public {

    }

    function createArticle(bytes32 title, bytes32 ID, address[] authorized) public {
        require(articles[title] == 0);

        titlesList.push(title);
        articles[title] = new Article(ID, msg.sender, authorized);
    }

    function nTitles() public view returns(uint) {
        return titlesList.length;
    }

    function getArticle(bytes32 title) public view returns(address) {
        return articles[title];
    }

}
