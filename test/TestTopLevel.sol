pragma solidity ^0.4.0;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "../contracts/TopLevel.sol";
import "../contracts/Article.sol";

contract TestTopLevel {
    TopLevel top = TopLevel(DeployedAddresses.TopLevel());

    function testAdd() public {
        top.createArticle(0x0, 0x000, new address[](0));
        top.createArticle(0x1, 0x111, new address[](0));
        top.createArticle(0x2, 0x222, new address[](0));

        Article a0 = Article(top.getArticle(0x0));
        Assert.equal(a0.getArticleID(), 0x000, "Article address do not match");
        Article a1 = Article(top.getArticle(0x1));
        Assert.equal(a1.getArticleID(), 0x111, "Article address do not match");
        Article a2 = Article(top.getArticle(0x2));
        Assert.equal(a2.getArticleID(), 0x222, "Article address do not match");
    }

    function testGetNotExisting() public {
        Assert.equal(top.getArticle(0x99), 0x0, "Non zero value for non-existing article");
    }
}
