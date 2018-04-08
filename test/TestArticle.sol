pragma solidity ^0.4.0;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "../contracts/Article.sol";

contract TestArticle {
    Article article = Article(DeployedAddresses.Article());

    function testModify() public {
        Assert.equal(article.getArticleID(), 0x2, "starting article id mismatch");

        article.modify(0x11);
        article.modify(0x12);
        article.modify(0x13);

        Assert.equal(article.nModifyRequests(), 3, "number of modifyRequests mismatch");
        Assert.equal(article.getArticleID(), 0x2, "article ID changed");

        var (ID1, Author1, votes1) = article.modifyRequests(0);
        var (ID2, Author2, votes2) = article.modifyRequests(1);
        var (ID3, Author3, votes3) = article.modifyRequests(2);

        Assert.equal(ID1, 0x11, "modify request ID mismatch");
        Assert.equal(ID2, 0x12, "modify request ID mismatch");
        Assert.equal(ID3, 0x13, "modify request ID mismatch");

        Assert.equal(Author1, this, "author mismatch");
        Assert.equal(Author2, this, "author mismatch");
        Assert.equal(Author3, this, "author mismatch");

        Assert.equal(votes1, 0, "number of votes not zero");
        Assert.equal(votes2, 0, "number of votes not zero");
        Assert.equal(votes3, 0, "number of votes not zero");
    }

    function testVote() public {
        article.modify(0x11);
        article.modify(0x12);

        Assert.equal(article.getArticleID(), 0x2, "starting article id mismatch");

        uint i;
        for (i = 0; i < article.RequiredVotes() - 1; i++) {
            article.vote(1);
        }

        for (i = 0; i < article.RequiredVotes(); i++) {
            article.vote(0);
        }

        // article 0 should be new main
        Assert.equal(article.getArticleID(), 0x11, "article id mismatch after voting");
        Assert.equal(article.nModifyRequests(), 0, "non zero number of modify requests");
    }
}
