library(tidyverse)

# Get the top 50 MSAs
population <- read_csv("data/census/ACS_15_5YR_DP05/ACS_15_5YR_DP05.csv", skip = 1) %>%
  select(c(Id2, Geography, `Estimate; SEX AND AGE - Total population`)) %>%
  rename(population = `Estimate; SEX AND AGE - Total population`) %>%
  arrange(desc(population)) %>%
  filter(Geography != "United States") %>%
  filter(row_number() <= 50)

# Table for joining airports to MSA
connect <- read_csv("data/flights/passenger_connectivity.csv") %>%
  filter(!is.na(AIRPORT_CODE),
         !is.na(CBSA_CODE),
         CBSA_TYPE == 1) %>%
  semi_join(population, by = c("CBSA_CODE" = "Id2")) %>%
  select(c(AIRPORT_CODE, #CITY, STATE,
           METRO_AREA, LONGITUDE, LATITUDE, CBSA_CODE))
# This is now a dataset that joins Airport Codes to Metro Area Names and codes

# Flight data
market_raw <- read_csv("data/flights/T100_dom_market.csv")

# Keep only itineraries that go from one of the top 50 MSAs to another of the top 50 MSAs
market <- market_raw %>%
  filter(PASSENGERS > 0) %>%
  select(c(PASSENGERS, ORIGIN, DEST)) %>%
  semi_join(connect, by = c("ORIGIN" = "AIRPORT_CODE")) %>%
  semi_join(connect, by = c("DEST" = "AIRPORT_CODE")) %>%
  # Add MSA info
  left_join(connect, by = c("ORIGIN" = "AIRPORT_CODE")) %>%
  left_join(connect, by = c("DEST" = "AIRPORT_CODE"), suffix = c("_origin", "_dest"))
market <- market %>%




market %>%
  arrange(ORIGIN_CITY_NAME) %>%
  filter(ORIGIN == "JFK" | ORIGIN == "LGA" | ORIGIN == "EWR") %>%
  View()

