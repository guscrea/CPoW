# 1 - Data coverage #

## How many data points are there in total? 
In total, we have over 3,000 unique county entries for analysis. There are no duplicates, as each has a unique county ID, and our data on religious denominations, voting patterns, and socioeconomic status was comprehensive.

## Any missing data?
Our dependent variable, the hate crime dataset, covers approximately 85% of the U.S. population, making it fairly representative. Originally, this data, sourced from the FBI, covered 93% of the U.S. population, with 7% of counties not reporting hate crimes. Our dataset has lower coverage (85%) because we excluded state-level and federal agency data, which couldn’t be mapped to counties.
Do you think this is enough data to perform your analysis later on?
Yes. Our dataset covers almost all 3,144 counties in the U.S, so there’s plenty of data to work with. Even without complete coverage on hate crime data, we can still perform valuable analysis on (1) hate crime patterns across the United States, and (2) patterns surrounding missing data.



# 2 - Data sourcing, processing, analysis, & ethics ###
_(Where is the data from? Comment on reputability, size, distribution, and possibility of skew or sampling bias. Any social / ethical considerations? Does it contain what you need in order to complete your proposed project?)_

## I - Election data: 
### SOURCE, REPUTABILITY, & ETHICAL CONSIDERATIONS:
Our election data is from the MIT Election Data & Science Lab, which publishes county presidential election returns from 2000 to 2020. This dataset is a cleaned aggregation of county-level votes that each state’s federal administration collected. All except Maryland, South Dakota, and Washington have been confirmed by MIT as official in their sources description in the Harvard Dataverse. 
To generate samples, we filtered to keep only 2020 data, and bucketed votes as “Democratic”, “Republican”, or “Other” - as third-party candidates were so diverse that there wasn’t any point trying to use them individually as predictive variables. While there was missing county data in earlier years, 2020 had no missing data. 
### DATA PROCESSING / CLEANING:
Missing votes from certain counties in less than 10 states. No missing votes from any state in 2020, but some missing votes in very early years.
No duplicate or data type issues, as data was pre-cleaned by MIT. 
Our only outlier was a region in Rhode Island labelled as “federal precinct”, with a small number of yearly votes, which had “N/A” as its FIP. As it was a very small region and presumably only a logistical grouping, we decided to throw it away: We couldn’t meaningfully match it with socioeconomic, religious, and racial metrics within the geographical location without a FIPS.

## II - religious census data:
### SOURCE, REPUTABILITY, & ETHICAL CONSIDERATIONS:
Our religious census data was sourced from ARDA (the Association of Religion Data Archives). ARDA is an authoritative archive platform, and the data was comprehensive, highly granular in terms of denomination, and didn’t need to be cleaned further. There were no privacy concerns - the data was anonymized, and licensed for public use with citation.
### DATA PROCESSING / CLEANING:
One big challenge was bucketing. The religion census raw data has a very high granularity, tracking hundreds of religious groups individually (e.g. by region, by denomination, by temple or church). If we kept these groupings, there would be too many factors to track for the purpose of our analysis. Therefore, informed by the categories of religious ‘families’ and ‘traditions’ on ARDA, we divided religions into nine large buckets. We grouped the many denominations into their respective buckets, then aggregated them.

## III - Hate crime data:
### SOURCE, REPUTABILITY, & ETHICAL CONSIDERATIONS:
Our hate crime data was collected by the FBI in 2019 as part of the Uniform Crime Reporting Program (UCR) - a national effort involving 18,000 law enforcement agencies who report crimes brought to their attention.
As a governmental source, this dataset is authoritative and credible; however, presumably due to the data’s sensitive nature, not all counties and organizations made data public. Additionally, since many hate crimes are self-reported, there was the possibility of reporting bias in different countries depending on social and political factors.
### DATA PROCESSING / CLEANING:
Since data was mainly numeric, cleaning meant checking for outliers that seemed like reporting mistakes - eg. decimals or strange values.
Missing values were present and documented in a separate table, corresponding to counties that didn’t report on 2019 hate crime data. The FBI notes that data from Alabama is particularly missing. This will inform our analysis later, but should not impact our overall data analysis since our scope is the entire nation, not specific state results.
We throw away counties with 25% or more of hate crime data missing. We also throwing away state and federal level data, since we can’t examine these at the county level. But again, this won’t damage the quality of our analysis too badly, as (1) we have many remaining data points, and (2) we plan on analyzing missing data to see if there are trends in the counties not reporting hate crimes.
Cleaning to join was a particularly tedious challenge: Since our dataset aggregated reports from cities, townships, boroughs, and other agencies (e.g. “x county police department”); we had to link these regions manually to counties (one of our primary keys aside from FIPS).

## IV - Socioeconomic data
### SOURCE, REPUTABILITY, & ETHICAL CONSIDERATIONS:
Our median personal income data comes from the U.S. Bureau of Economic Analysis (BEA), and our unemployment rate data comes from the USDA Economic Research Service (ERS). Both are authoritative, public government sources containing every US county; sampling bias is minimal because it is sourced from direct census reports. 
However, one limit is that economic data may not fully capture informal or underreported income sources, such as side gigs. Unemployment figures also may not take into account workers who have stopped actively seeking jobs or underemployment. 
### DATA PROCESSING / CLEANING:
Data cleaning: The income field initially contained non-numeric characters (commas, "(NA)") that required cleaning and conversion. No issues were found in unemployment data.
There were no duplicate records found, and our two datasets only had one missing value each - negligible, considering we have 3,000+ data points. 
Some of the datasets sometimes had different ways of naming and organizing regions - for instance, Virginia had counties, independent cities, and combined areas. Here, we kept counties with FIPS, but threw away data points about smaller regions, which were already listed under a reported county.

## Concluding thoughts & next steps
_Summarize any challenges or observations you have made since collecting your data. Then, discuss your next steps and how your data collection has impacted the type of analysis you will perform. (approximately 3-5 sentences)_
Originally, we aimed to analyze domestic abuse data but pivoted to aggregated hate crime data due to access restrictions. Due to reporting inconsistencies and data sensitivity, hate crime data was also challenging to collect at the county level - not all counties report their data, and federal datasets often lacked granular detail. There was also the concern of skewed results due to reporting bias - we hypothesized that, in liberal areas, victims of hate crimes might self-report at higher rates.
Another challenge was religious data bucketing: we categorized our religious affiliation groups into nine buckets, based on ARDA classifications, to manage the complexity of highly granular raw data.


	
