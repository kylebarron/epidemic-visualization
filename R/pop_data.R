library(tidyverse)
library(stringr)

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
# connect_2010data <- read_csv("data/flights/passenger_connectivity.csv") %>%
#   filter(!is.na(AIRPORT_CODE),
#          !is.na(CBSA_CODE),
#          CBSA_TYPE == 1) %>%
#   semi_join(pop_density, by = c("CBSA_CODE" = "Id2")) %>%
#   select(c(AIRPORT_CODE, #CITY, STATE,
#            METRO_AREA, LONGITUDE, LATITUDE, CBSA_CODE))

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

# Remove observations that have the same MSA as origin and dest
market <- market %>%
  filter(METRO_AREA_origin != METRO_AREA_dest)

# Sum up passengers from each origin to dest
market <- market %>%
  group_by(METRO_AREA_origin, METRO_AREA_dest) %>%
  mutate(total = sum(PASSENGERS)) %>%
  filter(row_number() == 1) %>%
  ungroup()

market <- market %>%
  select(METRO_AREA_origin, METRO_AREA_dest, total)

names <- market %>%
  group_by(METRO_AREA_origin) %>%
  filter(row_number() == 1) %>%
  arrange(METRO_AREA_origin) %>%
  select(METRO_AREA_origin) %>%
  ungroup() %>%
  rename(name = METRO_AREA_origin) %>%
  mutate(index = 1:50)

market_renamed <- market %>%
  left_join(names, by = c("METRO_AREA_origin" = "name")) %>%
  rename(origin = index) %>%
  left_join(names, by = c("METRO_AREA_dest" = "name")) %>%
  rename(dest = index) %>%
  select(origin, dest, total)

wide_index <- spread(market_renamed, dest, total)
wide_names <- spread(market, METRO_AREA_dest, total)
write_csv(wide_index, "data/adjacency_matrix.csv")
write_csv(wide_names, "data/adjacency_matrix_names.csv")
write_csv(names, "data/index_names.csv")



# Population Density Chart ------------------------------------------------

pop_density <- population %>%
  arrange(Geography) %>%
  mutate(pop_density = c(
    631.9,
    406.7,
    1041.9,
    213.7,
    1305.4,
    725.5,
    569.8,
    1314.6,
    485,
    1040,
    462.9,
    713.7,
    304.8,
    1104.9,
    800.5,
    673.7,
    455.6,
    420.4,
    260,
    247.3,
    2646,
    312.2,
    287.5,
    1096,
    1069.5,
    544.2,
    279.5,
    394.5,
    2826,
    227.3,
    613.6,
    1296.2,
    287.9,
    446.1,
    333,
    1008.8,
    533.7,
    221.3,
    155,
    421.9,
    117.7,
    293,
    735.8,
    1754.8,
    685.7,
    585.8,
    326.2,
    1107.3,
    635.7,
    997.1
  )) %>%
  left_join(
    connect %>% 
      group_by(CBSA_CODE) %>%
      filter(row_number() == 1),
    by = c("Id2" = "CBSA_CODE")
  ) %>%
  select(-c(AIRPORT_CODE, METRO_AREA, Id2)) %>%
  rename(city = Geography, lon = LONGITUDE, lat = LATITUDE)
write_csv(pop_density, "data/pop_density.csv")









  




