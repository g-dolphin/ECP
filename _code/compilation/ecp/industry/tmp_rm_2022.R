library(dplyr)
gversion<-"059"

## curr p | industry | edgar
df<-read.csv(file.path(here::here(),
                       "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                       "currentPrice","FlexXRate",
                       "ecp_gloria_edgar_industry_CO2.csv"))
df<-df %>% filter(year != 2022)
write.csv(df,file.path(here::here(),
                       "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                       "currentPrice","FlexXRate",
                       "ecp_gloria_edgar_industry_CO2.csv"),row.names=F)
rm(df)
## curr p | industry | oecd
df<-read.csv(file.path(here::here(),
                       "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                       "currentPrice","FlexXRate",
                       "ecp_gloria_oecd_industry_CO2.csv"))
df<-df %>% filter(year != 2022)
write.csv(df,file.path(here::here(),
                       "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                       "currentPrice","FlexXRate",
                       "ecp_gloria_oecd_industry_CO2.csv"),row.names=F)
rm(df)
## curr p | finaldem | edgar
df<-read.csv(file.path(here::here(),
                       "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                       "currentPrice","FlexXRate",
                       "ecp_gloria_edgar_finaldem_CO2.csv"))
df<-df %>% filter(year != 2022)
write.csv(df,file.path(here::here(),
                       "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                       "currentPrice","FlexXRate",
                       "ecp_gloria_edgar_finaldem_CO2.csv"),row.names=F)
rm(df)
## curr p | finaldem | oecd
df<-read.csv(file.path(here::here(),
                       "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                       "currentPrice","FlexXRate",
                       "ecp_gloria_oecd_finaldem_CO2.csv"))
df<-df %>% filter(year != 2022)
write.csv(df,file.path(here::here(),
                       "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                       "currentPrice","FlexXRate",
                       "ecp_gloria_oecd_finaldem_CO2.csv"),row.names=F)
rm(df)
## cons p | industry | edgar
df<-read.csv(file.path(here::here(),
                       "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                       "constantPrice","FixedXRate",
                       "ecp_gloria_edgar_industry_CO2.csv"))
df<-df %>% filter(year != 2022)
write.csv(df,file.path(here::here(),
                       "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                       "constantPrice","FixedXRate",
                       "ecp_gloria_edgar_industry_CO2.csv"),row.names=F)
rm(df)
## cons p | industry | oecd
df<-read.csv(file.path(here::here(),
                       "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                       "constantPrice","FixedXRate",
                       "ecp_gloria_oecd_industry_CO2.csv"))
df<-df %>% filter(year != 2022)
write.csv(df,file.path(here::here(),
                       "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                       "constantPrice","FixedXRate",
                       "ecp_gloria_oecd_industry_CO2.csv"),row.names=F)
rm(df)
## cons p | finaldem | edgar
df<-read.csv(file.path(here::here(),
                       "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                       "constantPrice","FixedXRate",
                       "ecp_gloria_edgar_finaldem_CO2.csv"))
df<-df %>% filter(year != 2022)
write.csv(df,file.path(here::here(),
                       "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                       "constantPrice","FixedXRate",
                       "ecp_gloria_edgar_finaldem_CO2.csv"),row.names=F)
rm(df)
## cons p | finaldem | oecd
df<-read.csv(file.path(here::here(),
                       "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                       "constantPrice","FixedXRate",
                       "ecp_gloria_oecd_finaldem_CO2.csv"))
df<-df %>% filter(year != 2022)
write.csv(df,file.path(here::here(),
                       "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                       "constantPrice","FixedXRate",
                       "ecp_gloria_oecd_finaldem_CO2.csv"),row.names=F)
rm(df)

