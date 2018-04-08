pragma solidity ^0.4.0;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "../contracts/Article.sol";

contract TestArticle {
    Article article = Article(DeployedAddresses.Article());

    function testModify() public {
        Assert.equal(article.getArticleID(), 0x2, "starting article id mismatch");
        Assert.equal(article.nModifications(), 1, "number of modifications mismatch");

        article.update(0x11);
        article.update(0x12);
        article.update(0x13);

        Assert.equal(article.nModifications(), 4, "number of modifications mismatch");
        Assert.equal(article.getArticleID(), 0x13, "article ID changed");
    }
}
