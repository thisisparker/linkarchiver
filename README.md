# LinkArchiver

[@LinkArchiver](https://twitter.com/linkarchiver) is a Twitter bot that allows Twitter users to automatically or interactively create snapshots in the Internet Archive's [Wayback Machine](https://web.archive.org/). When a user it follows tweets or retweets a link, @LinkArchiver will submit it to the Archive for a backup.

@LinkArchiver will follow anybody who follows it first. Once it is following you, you can optionally unfollow and it will continue to silently back up the links you tweet. To make that stop, block (and, optionally, unblock) the bot and it will stop following you.

You can also tweet a link directly to @LinkArchiver. If it's able to trigger a backup, it will respond within a few minutes with a link to that backup on the Internet Archiver.

If you want to run your own LinkArchiver bot, [register an app with Twitter](https://apps.twitter.com/), fill out config-sample.yaml, and rename it to config.yaml. You can initialize a new links.db database with the provided schema, or simply rename `renameaslinks.db` to links.db.
