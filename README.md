## **Things I've added:**

**Karma Points System**:  Give each other karma points with the "+karma @username" command. The bot tracks and displays the karma points for each user.

**Role Rewards**: Achieve specific karma thresholds to unlock special roles in the server. The bot automatically assigns roles based on users' karma scores. ( Although I don't think this is how it's handled normally)

**Star Roles**: As users gain more karma points, they can earn exclusive star roles.

**Karma Cooldown**: To maintain a fair and balanced karma system, users can use the "+karma" command once every 5 minutes to avoid spamming.

**Validity Checks**: The bot thoroughly verifies the mentioned user's existence before processing the karma command. If the user tagged is not real or not a valid mention, the bot promptly notifies the user for accurate interactions.

**Compatibility with Old Karma Bot**: Implemented a system to check users' previous karma scores from the old karma bot, if applicable, and update the local database with that information, with the command ".updatekarma"

## **Things I've yet to add**:



**Additional Karma Check Commands**: Check users' karma scores beyond the current "+karma lookup @username" or ".kc @username" command. Allow users to view their own karma points, the karma of others.


## **Things I could add:**

**Karma Leaderboard**: Create a command to display a leaderboard of users with the highest karma points. This can encourage friendly competition and engagement within the server.

**Karma Reset**: Implement a command for server administrators to reset a user's karma points. This can be useful if you want to start fresh or in cases where a user's karma needs to be adjusted.

**Karma Top**: Add a command to display the top users with the highest karma points. You can specify how many users to display in the leaderboard.

**Karma History**: Store and display a user's karma history, showing when they received karma and from whom. This can help track interactions and prevent misuse of the karma system.

**Customizable Cooldowns**: Allow server administrators to set custom cooldown times for the +karma command. Different karma actions might have different cooldowns.

**Role Removal**: Implement a command to remove a specific karma role from a user if necessary.

**User Karma Lookup**: Allow users to check their own karma points or the karma points of other users using a command.
