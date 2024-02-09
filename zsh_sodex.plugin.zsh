#!/bin/zsh

# This ZSH plugin reads the text from the current buffer 
# and uses a Python script to complete the text.
 

sodex_create_completion() {
    # Get the text typed until now.
    text=${BUFFER}
    #echo $cursor_line $cursor_col
    completion=$(echo -n "$text" | $ZSH_CUSTOM/plugins/zsh_sodex/create_completion.py $CURSOR)
    text_before_cursor=${text:0:$CURSOR}
    text_after_cursor=${text:$CURSOR}
    # Add completion to the current buffer.
    #BUFFER="${text}${completion}"
    BUFFER="${text_before_cursor}${completion}${text_after_cursor}"
    prefix_and_completion="${text_before_cursor}${completion}"
    # Put the cursor at the end of the completion
    CURSOR=${#prefix_and_completion}
}

# Configuration of the plugin.
# Check if zsodex_config exists as a function and source it.
if functions -t zsodex_config; then
    zsodex_config
else
    # inform the user it needs a config function before using the plugin
    echo "zsodex: You need to define a zsodex_config() function in your .zshrc"
fi

# Bind the create_completion function to a key.
zle -N sodex_create_completion