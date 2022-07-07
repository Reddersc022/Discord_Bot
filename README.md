# Discord_Bot

by: @ch0rl, chorl#2222  
bot: Charlie's bot#3117


COMMANDS:
Keyphrase | Explanation
--------- | -----------
help | Displays the help message
kill ... | If provided with the correct token, stops execution
addcom <0> ... | Adds command <0> that responds with `...` . Anywhere in `...`, {} can be used to enclose formatting specifiers. These specifiers are: any integer - referring to the nth word *after* the command (0-indexed), and author - referring to the person invoking the command. For example, `!c addcom !hi hello {author}` would add a command that replies to `!hi` with `hello` and then the author's display name.
editcom <0> ... | Effectively the same as above
delcom <0> | Removes command <0>

Help from:  
https://realpython.com/how-to-make-a-discord-bot-python/  
Code:  
https://github.com/ch0rl/Discord_Bot
