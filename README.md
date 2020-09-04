# ODI Token Contracts

OpenDevICON Token Contracts implement IRC2 standard token which is equivalent to [ERC20](https://eips.ethereum.org/EIPS/eip-20) for [ICON](https://icon.foundation/?lang=en) blockchain. It helps to keep track of [fungible](https://en.wikipedia.org/wiki/Fungibility) tokens.

There are a few core contracts to implement IRC2 token.

-   [IIRC2](https://github.com/icon-project/IIPs/blob/master/IIPS/iip-2.md): Interface IRC2 methods should confirm into.
-   [IRC2](https://docs.opendevicon.io/v/development/score-library/irc2standard): The base implementation of IRC2 contract.

This has been extended to implement the following.

-   [IRC2Mintable](https://docs.opendevicon.io/v/development/score-library/irc2standard/irc2mintable): To create token supply.
-   [IRC2Capped](https://docs.opendevicon.io/v/development/score-library/irc2standard/irc2capped): Total supply cannot exceed the cap amount.
-   [IRC2Burnable](https://docs.opendevicon.io/v/development/score-library/irc2standard/irc2burnable): To destroy the tokens.
-   [IRC2Pausable](https://docs.opendevicon.io/v/development/score-library/irc2standard/irc2pausable): To pause token operation for all users.
-   [IRC2Snapshot](https://docs.opendevicon.io/v/development/score-library/irc2standard/irc2snapshot): To add snapshot mechanism.

> Visit [OpenDevICON]("https://docs.opendevicon.io/v/development/") for more info.
<<<<<<< HEAD

## IRC3
OpenDevICON Token Contracts implement IRC3 standard token which is equivalent to [ERC721](https://eips.ethereum.org/EIPS/eip-721) for [ICON](https://icon.foundation/?lang=en) blockchain. It helps to keep track of [non-fungible] tokens.

There are a few core contracts to implement IRC3 token.

-   [IIRC3](https://github.com/icon-project/IIPs/blob/master/IIPS/iip-3.md): Interface IRC3 methods should confirm into.
-   IRC3: The base implementation of IRC3 contract.

This has been extended to implement the following.

-   IRC3Mintable: To create non-funglible token.
-   IRC3Burnable: To destroy the non-fungible token.
-   IRC3Pausable To pause token operation for all users.
-   IRC3Updatable: To update the created non-fungible tokens.
