# Scripts

Right now, I'm putting here a list of the scripts that I upload, with a brief description.
They are separated by folders by themes.
Probably not a production quality code, but they work for me, and maybe they can be useful for you too.
I will tag them with the language they are written in. Everything is intended to work on Linux, I don't know if they will work on Windows.


## Easier logs

- `coloredtail.sh` [bash] - A tail with colors, to make it easier to read logs. It follows a regex.
- `filterByHours.py` [python] - Return a summary of the runtime of a program, 1 line per hour (01:00:00, 02:00:00, and so on).
  

## Git

- `commit.sh` [bash] - This is a [Gum](https://github.com/charmbracelet/gum) script, I love it. It's a wrapper for git commit, with a cute interface to write title and body.

## Ethereum

- `deploy.py` [python] - Deploy a contract to target network configured in `hardhat.config.js`, it recieves the name of the contract, the constructor args and the network to deploy to.