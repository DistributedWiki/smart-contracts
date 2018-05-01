var Article = artifacts.require("./Article.sol");
var TopLevel = artifacts.require("./TopLevel.sol");

module.exports = function(deployer) {
    deployer.deploy(Article, "0x0000000000000000000000000000000000000000000000000000000000000002".valueOf());
    deployer.deploy(TopLevel);
};
