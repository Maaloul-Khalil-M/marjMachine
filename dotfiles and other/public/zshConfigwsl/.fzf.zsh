# Setup fzf
# ---------
if [[ ! "$PATH" == */home/marj/.fzf/bin* ]]; then
  PATH="${PATH:+${PATH}:}/home/marj/.fzf/bin"
fi

# Auto-completion
[[ $- == *i* ]] && source "/home/marj/.fzf/shell/completion.zsh" 2> /dev/null

# Key bindings
source "/home/marj/.fzf/shell/key-bindings.zsh"
