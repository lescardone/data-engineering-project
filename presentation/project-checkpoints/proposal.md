# DATA ENGINEERING: Automating The Collection of Data Science Job Postings

## Question/Need:
*What is the framing question of your analysis, or the purpose of the model/system you plan to build?*

- What are the trends in job postings skills and requirements for Data Science or similar roles over time

*Who benefits from exploring this question or building this model/system?*  

Anyone in a Data Science bootcamp or persuing a Data Science career path would benefit from knowing what skills are being asked for and how those skills requirements might be changing over time.

## Data Description:
*What dataset(s) do you plan to use, and how will you obtain the data?*  

I would like to figure out a way to webscrape the data from [Indeed](https://www.indeed.com/), Linkedin, [Ziprecuriter](https://www.ziprecruiter.com/Search-Jobs-Near-Me), [Angelist](https://angel.co/company/angellist/jobs) or make use of an API.

I am looking at [this Indeed API](https://rapidapi.com/indeed/api/indeed/). I have already requested an [Indeed Publisher ID](https://pubwebapp.indeed.com/jobroll/traffic).

*What is an individual sample/unit of analysis in this project? What characteristics/features do you expect to work with?*

One sample would be one job posting including all the listed skills, required experience, location, job title, etc.

## Tools:
*How do you intend to meet the tools requirement of the project?*
- Store Data in Google Cloud
- Build a Flask Web App

*Are you planning in advance to need or use additional tools beyond those required?*
- Unsure

## MVP Goal:
*What would a minimum viable product (MVP) look like for this project?*
- Successful API request or webscrape script
- Set up basic workflow for storing files in Google Cloud buckets
- Google Cloud scheduler?