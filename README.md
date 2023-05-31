# Scripts

> _This could be a "gist collection", "script toolbox" or something like that_

I'm putting here a list of the scripts that I upload, with a brief description.
They are separated by folders by themes.

Not a production quality code, but they work for me, and maybe they can be useful for you too.

I will tag them with the language they are written in. Everything is intended to work on Linux, I don't know if they will work on Windows.

You are free to modify and use them, modify them, update them, or whatever you want.


## Easier logs

- `coloredtail.sh` _(bash)_ - A tail with colors, to make it easier to read logs. It follows a regex.
- `filterByHours.py` _(python)_ - Return a summary of the runtime of a program, 1 line per hour (01:00:00, 02:00:00, and so on). This is intended for the same output as `coloredtail.sh`.
  

## Git

- `commit.sh` _(bash)_ - This is a [Gum](https://github.com/charmbracelet/gum) script, I love it. It's a wrapper for git commit, with a cute interface to write title and body.

## Ethereum

- `deploy.py` _(python)_ - Deploy a contract to target network configured in `hardhat.config.js`, it recieves the name of the contract, the constructor args and the network to deploy to.