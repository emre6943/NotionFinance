## Your .env should look like this

SECRET_TOKEN=(secret token from notion api)
DATABASE_ID=(the id of the database, you can see in the link if you fo to that table)

TL=(currency Id if you go to that pages link you can find it in the link)
EUR=(currency Id if you go to that pages link you can find it in the link)

## you need the chrom driver
install a chrome driver for your os and chrome version => https://chromedriver.chromium.org/downloads

put the chrome driver location inside FinanceApi line 14 => yea I know I should have put that into env to but it is only used there so stop crying

## Test
Test if it works by runing the Notion Api, 
You can remove the web driver options (in FinanceApi line 10 - 12) for testing

## Set up the cron job for Updating
I set mine up for once every hour, I would suggest testing and seeting how long does it actually take for it to finish
for me it takes around 10 mins but this changes with the size of the watchlist,
so just check the run time and make sure to not set the cron job for faster than it runs

## Questions
For questions just comment to my video => 
and while you are there liking would make my day :*