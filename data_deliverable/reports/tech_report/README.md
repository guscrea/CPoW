# README (tech report)

How many data points are there in total?
We have over 3,000 unique county entries for analysis. 1,653 county-level data points include hate crime data, but 1,500 of our county-level data points are missing hate crime data.
In total, we have over 3,000 unique county entries for analysis. There are no duplicates, as each has a unique county ID. Our dataset with hate crime data covers approximately 85% of the U.S. population, making it fairly representative.
Originally, the FBI data covered 93% of the U.S. population, with 7% of counties not reporting hate crime data. Our dataset has lower coverage because we excluded state-level and federal agency data, as these cannot be mapped to counties.

1653 county entry data points with hate crime data
1500 county data points with missing hate crime data
In total more than 3000+ entries we can analyze (with no duplicates snice unique county ids)
Our data with hate crime data covers approx 85% of the us population (so failry representative) → originally the fbi data covered 93% of the us population, with 7% not have reported hate crime data, we have lower amounts because we threw out state-level and federal agency data because we can’t split those to the county level
Do you think this is enough data to perform your analysis later on?
Our dataset covers all 3144 counties in the U.S., so plenty of data.
We have missing hate crime data. This is cos not all counties report their hate crime data + some of the data is gathered at state or federal level, so cannot be granularized to county level
Some attributes of hate crime data might be missing (due to sensitive nature), but the elections & religious groups data are comprehensive.
What are the identifying attributes?
County FIPS as primary key

Data sources:
Religion census data from ARDA(Association of Religion Data Archives)
Authoritative archive platform
Very comprehensive, large sample size, highly granular
Consent to usage as long as there’s proper citation
Clean raw data, did not require cleaning.
Hate crime data from FBI, collected in 2019 with their UCR data reporting
Also authoritative and credible source / reputable since comes from a governmental agency
Election data from \_\_\_\_
Socio-economic data from the U.S. Bureau of Economic Analysis (BEA) and the USDA Economic Research Service (ERS).
Sample info:
The sample of 100 data points that they want was just taken from the first 100 entries in counties_data, ordered by county_fips. This is in no way representative of the US and the data as a whole, as this means these counties are primarily belonging to the first states when in alphabetical order of the US.
However, if they mean the overall data, it is representative of the population as a whole (aka the country) since we have representation from most counties in the US. The risks of sampling bias include the risks associated with the census, falsified data (lower reporting than the truth) because hate crimes are not always reported to governmental agencies, and bias in that some states may be more likely not to report their hate crime data.

Cleanliness:
For the FBI hate crime data
Since data mainly numeric, cleanliness of data meant checking for odd outliers (potential reporting mistakes), weird decimals when everything is supposed to be an int, etc.
Missing values are present and documented, these correspond to counties that did not report on hate crime data during 2019. The FBI notes that data from Alabama is particularly missing for the 2019 data. This will inform our analysis later, but should not impact our overall data analysis since we’re looking at the country/national level scope, not comparing state results
Duplicates occur maybe? Like the values might be the same for certain things, but that’s normal. There are no duplicate counties though because unique on county_fips
We’re throwing the missing hate crime counties data away for analysis on predicting hate crime counts, but this once again shouldn’t affect us too badly since we’re not missing that much data. We are still planning on analyzing missing data to figure out if there are any trends in the counties not reporting on hate crimes. All counties who had at least one quearter’s report missing hate crime data was counted as a county not reporting on hate crime data. We’re also throwing away state and federal level data since we cannot examine these at county level.
Oh my god main cleaning/joining challenge was the INSANE way I had to try to link random parts of the county to the overall county. Cos there wasn’t just counties and cities as entires, there were random boroughs, townships, etc. etc. + the names don’t correspond one to one to the city or county, since the entry was for the agency name, so I would get “x county police department” so I couldn’t join directly on a county name to fips dataset omg I hated this so bad

Sensitive data: sadness :( we couldn’t use the original domestic abuse data we wanted due to access issues (needing to go through irb reporting etc. because of the sensitivity of the data). This made us pivot towards aggregated hate crime data instead. However, due to the sensitivity of the ; + granularity of the data difficult because it’s sensitive (most data at state-level and aggregated, very difficult to hone down even to the county level)
Underreporting: Also because it’s sensitive/other factors at play, many places will underreport or not report hate crime data. While things have improved lately with increased regulation (90%+ of the American population is covered by the FBI hate crime dataset, and 85% of the population with our dataset), this still shines a light on how difficult acquiring this data is
Grouping challenges: the religion census raw data has a very high granularity, tracking hundreds of religious groups individually. If we keep these groupings, there would be too many factors to track for the purpose of our analysis. Therefore, informed by the categories of religious ‘families’ and ‘traditions’ on ARDA(Association of Religion Data Archives), we divided religions into nine large buckets. We group the raw data into their respective buckets, then aggregate them.
