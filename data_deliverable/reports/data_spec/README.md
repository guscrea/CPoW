# README (data spec)

## The datasets we cleaned and joined were:
“County Presidential Election Returns 2000-2020” from the MIT Election Data and Science Lab in 2018, which collected federal data from each state.
(Provided voting data and county identifier data (except for county population))
“Hate Crime Incidents, per Bias Motivation and Quarter, by State, Federal, and Agency, 2019” from the FBI, 2019
(Provided hate crime data)
the ARDA US Religion Census 2020 dataset
(Provided religious adherence data and population per county)
the U.S. Bureau of Economic Analysis (BEA)
(Provided median household income per county)
the USDA Economic Research Service (ERS).
(provided unemployment rate per county)

We joined these datasets with county FIPS and county name as our primary keys. Since MIT’s dataset had an exhaustive list of FIPS associated with cleaned county names, we used it as a reference when identifying missing values and cleaning inconsistent entered county names by hand.

## all data attributes:
### a. county_fips - int, primary key of table

A unique identifier for each county used by the US government for identification. Ensures there are no duplicate rows in the table. Ranges from 1073 to 56041 in the counties_data dataset, and 1001 to 56045 in the misisng_counties dataset (overall, ranges from 1001 to 56045 and covers all US counties). It does not make sense to analyze the distribution of values since this is a county identifier. This is a required value and will be used in our analysis to identify any duplicate data as well as associate any findings with the correct counties.

### b. state - text, US state name, fully capitalized. Drawn from the US Census 2020 election dataset.

### c. county_name - text, US county name, fully capitalized. Drawn from the US Census 2020 election dataset.

### d. population - int, number of residents for county county_name in state in 2020. Drawn from the ARDA US Religion Census 2020 dataset.
Range: 64 to 10,014,009
Distribution: Highly positively skewed (right-skewed)
The data shows extreme variation with a few very large values (likely major metropolitan counties) and many smaller values. Appears to follow a power law distribution typical of population data. Does not contain sensitive data. We plan to use this data in our analysis to normalize the number of hate crimes per county.

###  e. democrat_votes - int, number of …

###  f. republican_votes - int, number of …
### g. other_votes - int, number of …

###  h. Mainline Protestant_adh - adherents to mainline Protestantism per 1000 people in a county. Drawn from the ARDA US Religion Census 2020 dataset.
Range: 0 to 501.98  
Distribution: Positively skewed
Wide variation in adherence rates across counties
Smaller range than Other Christian Denominations.

### i. Liturgical/Traditional_adh - adherents to Liturgical/Traditional per 1000 people in a county. Drawn from the ARDA US Religion Census 2020 dataset.
Range: 0 to 287.37
Distribution: Positively skewed
Most counties have lower adherence rates with a few areas of concentration.

### j. Evangelical/Fundamentalist_adh -  adherents to Evangelical/Fundamentalist per 1000 people in a county. Drawn from the ARDA US Religion Census 2020 dataset.
Range: 0 to 376.98
Distribution: Positively skewed
Moderate range compared to other Christian categories.

### k. Other Christian Denominations_adh - adherents to other Christian denominations per 1000 people in a county. Drawn from the ARDA US Religion Census 2020 dataset.
Range: 0 to 480.6
Distribution: Positively skewed
Most counties have relatively low adherence rates, with a few counties showing very high rates. Suggests geographic concentration of certain denominations. Does not contain sensitive data, as it was collected through the US census (so public information) and is aggregated by county. We plan to use this data in our analysis to see how well this predicts the number of hate crimes in each county.

### l. Judaism_adh - adherents to Judaism per 1000 people in a county. Drawn from the ARDA US Religion Census 2020 dataset.
Range: 0 to 19.17
Distribution: Extremely positively skewed
Most counties have very low or zero adherence rates. A few counties have notably higher concentrations.

### m. Hinduism_adh - adherents to Hinduism per 1000 people in a county. Drawn from the ARDA US Religion Census 2020 dataset.

Range: 0 to 7.06
Distribution: Extremely positively skewed
Very low adherence rates in most counties.Likely concentrated in specific geographic areas.

## n. Buddhism_adh - adherents to Buddhism per 1000 people in a county. Drawn from the ARDA US Religion Census 2020 dataset.
Range: 0 to 4.11
Distribution: Extremely positively skewed
Very low adherence rates across most counties. Most limited range of all religious categories.

## o. Islam_adh - adherents to Islam per 1000 people in a county. Drawn from the ARDA US Religion Census 2020 dataset.
Range: 0 to 70.47
Distribution: Extremely positively skewed
While still showing geographic concentration, has a wider range than other non-Christian religions. Most counties show low adherence rates.

## p. Other_adh - adherents to other religions per 1000 people in a county.
Range: 0 to 675.78
Distribution: Positively skewed
Shows considerable variation across counties.

## q. median_income (USD) -  median household income per county (USD)
Range: 1.6 to 22.6
Distribution: Positively skewed
Varies widely across counties. Does not contain sensitive data, as it was collected through the US census (so public information) and is aggregated by county. We plan to use this data in our analysis to see how well this predicts the number of hate crimes in each county.

## r. unemployment_rate - county unemployment rate (%)
Range: 21,087 to 220,645
Distribution: Positively skewed
Shows significant variation across counties. Suggests possible correlation between economic disparities and hate crime rates. 

## s. race_ethnicity_ancestry - int, number of hate crimes related to race, ethnicity, or ancestry of victim
Ranges from 0 to 236. Positively skewed, with a mean of 4.3 across all counties in counties_data (meaning with hate crime data present). Shows considerable variation across counties.

## t. religion - int, number of hate crimes related to religion of victim
Ranges from 0 to 271. Positively skewed, with a mean of 1.7 across all counties in counties_data (meaning with hate crime data present). Shows some variation across counties.

## u. sexual_orientation - int, number of hate crimes related to sexual orientation of victim
Ranges from 0 to 98. Positively skewed, with a mean of 1.3 across all counties in counties_data (meaning with hate crime data present). Shows little variation across counties.

## v. disability - int, number of hate crimes related to disability of victim
Ranges from 0 to 9. Positively skewed, with a mean of 0.17 across all counties in counties_data (meaning with hate crime data present). Shows little variation across counties.

## w. gender - int, number of hate crimes related to gender of victim
Ranges from 0 to 6. Positively skewed, with a mean of 0.07 across all counties in counties_data (meaning with hate crime data present). Shows little variation across counties.

## x. gender_identity - int, number of hate crimes related to gender identity of victim
Ranges from 0 to 27. Positively skewed, with a mean of 0.2 across all counties in counties_data (meaning with hate crime data present). Shows little variation across counties.

## y. num_crimes - int, total number of hate crimes in 2019 per county, as collected by the FBI UCR dataset.

All counties with missing data were excluded from counties_data and placed into missing_counties instead. As such, there is no default value. The data ranges from 1 to 429, with a mean of 7.8. Values are not necessarily unique, but records cannot be duplicates as there is one entry per county at most. This is a required value for our analysis since we want to predict this number based on all of our other factors.

## Sample of data: 
https://docs.google.com/spreadsheets/d/1yv4t5qT4fFREVVFKIKmlDRW059YdiRkwuu__yQDo-8I/edit?usp=sharing
Here is a link to the first 90+ rows of our data in Google Sheets. 
