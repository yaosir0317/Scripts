#!/bin/bash

# install homebrew
date
echo "install homebrew"
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

# install git
date
echo "install git"
brew install git


# install gun sed
date
echo "install gun sed"
brew install gnu-sed --with-default-names

# install iterm2
date
echo "install iterm2"
brew cask install iterm2
echo "install oh my zsh"
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
chsh -s /bin/zsh
sed '/^ZSH_THEME=/c\ZSH_THEME=\"agnoster\" \nwestos' ~/.zshrc
echo "download solarized manually please"
echo "download url: http://ethanschoonover.com/solarized; then import and set"
echo "Profiles -> Colors -> Color Presets -> Import ==> solarized->iterm2-colors-solarized->Solarized Dark.itermcolors"
echo "download Meslo LG M Regular for Powerline.ttf font manually please"
echo "download url:  https://github.com/powerline/fonts"
echo "Profiles -> Text -> Font -> Chanage Font"
echo "install highlighting"
brew install zsh-syntax-highlighting
echo "source /usr/local/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" >> ~/.zshrc
echo "install auto-suggestions"
git clone https://github.com/zsh-users/zsh-autosuggestions ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions
echo "vim ~/.zshrc -> add zsh-autosuggestions to plugins manually please"

# install redis
brew install redis

# install pyenv
brew install pyenv
echo export PATH="$HOME/.pyenv/bin:$PATH" >> ~/.zshrc

# docker
echo "download docker url: https://download.docker.com/mac/stable/Docker.dmg"
