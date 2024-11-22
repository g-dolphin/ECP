# Maps


library(dplyr)
library(ggplot2)

wd<-file.path(here::here(),"_code","compilation","ecp","industry")
setwd(wd)


cbase="edgar" 
pl="curr_p"
gversion="059"

dfz<-read.csv(file.path(here::here(),
                        "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                        "currentPrice","FlexXRate",
                        "ecp_gloria_edgar_industry_CO2.csv"))
dfz$ecp_edgar[is.na(dfz$ecp_edgar)]<-0
dfz <- dfz %>% rename(ecp=ecp_edgar)
dfz <- dfz %>% rename(co2_total = co2_edgar_total)
dfy<-read.csv(file.path(here::here(),
                        "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                        "currentPrice","FlexXRate",
                        "ecp_gloria_edgar_finaldem_CO2.csv"))
dfy$ecp_edgar[is.na(dfy$ecp_edgar)]<-0
dfy <- dfy %>% rename(ecp=ecp_edgar)
dfy <- dfy %>% rename(co2_total = co2_edgar_total)
dfy <- dfy %>% filter(sector == "Household final consumption P.3h")

# merge dfy and dfz and filter what we need
yr<-2021
df<-rbind(dfz,dfy) %>% filter(year==yr) %>% select(c(country,sector,ecp,co2_total))

# emissions-weighted prices by country
df<-df %>% mutate(ecpw = ecp*co2_total)

dfs<-df %>% group_by(country) %>% summarise(ecpw=sum(ecpw),co2_total=sum(co2_total))
dfs<-dfs %>% mutate(ecp=ecpw/co2_total)
dfs<-dfs %>% filter(ecp>0)
dfs$country[dfs$country=="CSSR/Czech Republic (1990/1991)"]<-"Czech Republic"


#
library(ggthemes)

world_map <- map_data("world") %>% filter(!long > 180)

mapctrs<-unique(world_map$region)

world_map['ecp']<-0

for(i in 1:nrow(dfs)){
  world_map$ecp[world_map$region==dfs$country[i]]<-dfs$ecp[i]
}

world_map['zero']<-"zero"
world_map$zero[world_map$ecp>0]<-"non-zero"

gg<-ggplot(world_map,aes(fill=ecp, map_id=region, alpha=zero)) +
  geom_map(map=world_map) +
  scale_fill_viridis_c() +
  scale_alpha_manual(values=c(1,0.1)) +
  expand_limits(x = world_map$long, y = world_map$lat) +
  coord_map("moll") +
  theme_bw() +
  labs(title="Average marginal cost of emitting carbon 2021",
       fill="USD",
       caption="Emissions-weighted carbon prices, Dolphin & Merkle (2024)") +
  theme(legend.position=c(0.05,0.8),
        axis.text = element_blank(),
        axis.title = element_blank())+
  guides(alpha='none')

ggsave(gg,filename=paste0("ecp_map_",yr,".svg"),
       device="svg",
       height=5,
       width=10,
       path=file.path(wd,"3_checks",pl,cbase,"map"))




