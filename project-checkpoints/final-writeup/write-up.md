# **STARTING A LANE HOUSE RENTAL PROPERTY PORTFOLIO IN SHANGHAI**
Leslie Cardone  
April 30, 2021  
Metis: Business Fundamentals



## ABSTRACT

There is a niche market in Shanghai, China where property management companies will seek out long term leases with owners of the European-style houses in the Former French Concession. These house, built from the late 1800s to the early 1930s are now in a state of disrepair. 

The management companies invest money to fix and renovate apartments in these houses. The newly renovated apartments are then marketed and rented out, at a higher price, to international (and local) professionals in the city. 

The goal of this project is to analyze this rental market and identify a profitable entry point for an interior design and management start-up. 

I hypothesized that there are opportunities to enter this market, and that we would find our target properties in less saturated areas of Shanghai.


## DATA

I collected the data for this study from the open source listing website [Jia Zai Shanghai](https://www.jiazaishanghai.com).

I was able to 'scrape' about 5,000 samples of our target apartments (attached lane houses, detached lane houses, and concrete walk-ups). This website and its listings are not strictly regulated. The data contained invalid addresses, invalid pricing information, and duplicated listings, among other issues.

I worked between using [Google Sheets](https://docs.google.com/spreadsheets/d/1Jpm2tPldOSDbgxkrSbyIXOZbSTx4Vu2PwcaLCxrOH_M/edit?usp=sharing) and Python to remove invalid entries and duplicated listings. In the end I had a data set of about 2,500 apartments.

## DESIGN

I used geocode.xyz to obtain latitude and longitude for the addresses. I plotted these coordinates on a map and also analyzed the apartments by district, rent, and house type.


## ALGORITHMS/TOOLS

*LIBRARIES*
- Selenium and BeautifulSoup for webscraping
- Numpy and Pandas for data manipulation
- Google Sheets for data cleaning
- Tableau for visualizations


## COMMUNICATION
*VISUALIZATIONS*
1. Number of apartments (for rent and already rented) by district:


![image](../presentation/images/graphs/listings_by_district_xuhui.png)


2. Distribution of rent in Xuhui


![image](../presentation/images/graphs/xuhui_distplot.png)


3. Map of foreign settlements in Shanghai 1937

![image](../presentation/images/graphs/foreign_settlements_1937.jpg)


4. Map of foreign settlements in Shanghai 1904
![image](../presentation/images/graphs/map_foreign_settlements_sh2.jpg)


5. Map of apartments (size indicates number of apartments in that area)
![image](../presentation/images/graphs/listings_district_map.png)
