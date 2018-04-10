var Article = artifacts.require("./Article.sol");

module.exports = function(deployer) {
    deployer.deploy(Article, 0x1, "0x0000000000000000000000000000000000000000000000000000000000000002".valueOf());
};
