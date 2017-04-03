# collectionScripts
These scripts are being created as a first step of the project to allow University of Illinois researchers to better
access and analyze social media data for their research projects.

The scripts in the folder labeled Crimson are for attaching to the API of the social media analytics service Crimson Hexagon.
This is a paid service contacted by the University untill 8/1/17. To use this script you'll need our api key which you can
sign up to access at go.illinois.edu/UseCrimsonHexagon

The scripts in the network analysis folder are for analyzing already downloaded social data to find network connections in
the mentioning or retweeting of other accounts within the data sample.

The Twitter Streaming API folder is a collection of scripts to collect data from the Twitter Public Streaming API and write
it to various data collection methods.
Those labeled sample collect from the Twitter selected 1% sample stream.
Those labeled filter collect from the filter stream and require the addition of search keywords to identify data.
The filter stream will provide all of the data on specific keywords until the volume reaches 1% of the current total volume of Twitter posts.
All of these scripts will require the addition of Twitter API keys to work and some require authentication credentials
for the various storage applications they write to.

Any questions on these scripts can be directed to Nick Vance at npvance2@illinois.edu
