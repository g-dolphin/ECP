# Maps


library(dplyr)
library(ggplot2)

wd<-file.path(here::here(),"_code","reporting","charts")
setwd(wd)


# get ecp by location
dfa<-read.csv(file.path(here::here(),"_output","_dataset","ecp","ipcc","ecp_economy","ecp_CO2.csv")) %>% 
  filter(year==2024) %>% select(-year) %>% select (c(jurisdiction,ecp_all_jurCO2_usd_k)) %>%
  filter(ecp_all_jurCO2_usd_k>0)

# get max price for each
dfm <- read.csv(file.path(here::here(),"_output","_dataset","ecp","ipcc","ecp_ipcc","constantPrices","FixedXRate","ecp_ipcc_CO2_kFixRate.csv")) %>%
  filter(year==2024) %>% mutate(ecp_all_corr = ecp_all_usd_k/CO2_shareAggSec) %>%
  select(c(jurisdiction,ipcc_code,ecp_all_corr)) %>% group_by(jurisdiction) %>%
  summarise(cp_max = max(ecp_all_corr))

# then join
df<- left_join(dfa,dfm,by="jurisdiction")

# I add a procedure for Canada and US
df['Canada']<-NA
df$Canada[df$jurisdiction %in% c("Alberta","British Columbia","Saskatchewan",
                                 "Prince Edward Island","Yukon","Nova Scotia","Nunavut",
                                 "Quebec","Newfoundland and Labrador","Ontario",
                                 "New Brunswick","Manitoba",
                                 "Northwest Territories")] <- "yes"

df['usa']<-NA
df$usa[df$jurisdiction %in% c("California","Connecticut","Maryland","New Jersey",
                              "Massachusetts","New York","Maine","Vermont",
                              "Rhode Island","Washington","Colombia","Delaware",
                              "New Hampshire")] <- "yes"


df$cp_max[df$jurisdiction=="Canada"]<-df %>% filter(Canada=="yes") %>% 
  select(ecp_all_jurCO2_usd_k) %>% max()

df$cp_max[df$jurisdiction=="United States"]<-df %>% filter(usa=="yes") %>% 
  select(ecp_all_jurCO2_usd_k) %>% max()

# then filter
df <- df %>% filter(is.na(Canada)) %>% filter(is.na(usa)) %>% select(-c(Canada,usa))
df <- df %>% filter(jurisdiction != "World")


# get world map
library(ggthemes)

world_map <- map_data("world") %>% filter(!long > 180)

mapctrs<-unique(world_map$region)

world_map['ecp']<-0
world_map['cpm']<-0

# check if we have all ecp countries in the world map
df$jurisdiction[!df$jurisdiction %in% unique(world_map$region)]
# ok there are a few we need to rename

unique(world_map$region)
df$jurisdiction[df$jurisdiction=="Korea, Rep."]<-"South Korea"
df$jurisdiction[df$jurisdiction=="Slovak Republic"]<-"Slovakia"
df$jurisdiction[df$jurisdiction=="United Kingdom"]<-"UK"
df$jurisdiction[df$jurisdiction=="United States"]<-"USA"

# and then we put the carbon price data into our world map
world_map <- world_map %>% left_join(df,by = join_by(region==jurisdiction))

# and create a variable carbon price variation
world_map <- world_map %>% mutate(cp_var = (cp_max-ecp_all_jurCO2_usd_k)/cp_max)



### MM note: 
# there is a problem with south africa. Economy ECP is higher than the highest sectoral price
# to check with GD. For the time being I correct this manually.

world_map$ecp_all_jurCO2_usd_k[world_map$region=="South Africa"] <- 11.76

# and create a variable carbon price variation again
world_map <- world_map %>% 
  mutate(cp_var_rel = (cp_max-ecp_all_jurCO2_usd_k)/cp_max) %>%
  mutate(cp_var_abs = cp_max-ecp_all_jurCO2_usd_k)
  

# South Africa's ecp might still be incorrect, let's check later



world_map['zero']<-"zero"
world_map$zero[world_map$ecp_all_jurCO2_usd_k > 0]<-"non-zero"

gg1<-ggplot(world_map,aes(fill=ecp_all_jurCO2_usd_k, map_id=region, alpha=zero)) +
  geom_map(map=world_map) +
  scale_fill_viridis_c() +
  scale_alpha_manual(values=c(1,0.1)) +
  expand_limits(x = world_map$long, y = world_map$lat) +
  coord_map("moll") +
  theme_bw() +
  labs(title="Average marginal cost of emitting carbon 2024",
       fill="USD",
       caption="Emissions-weighted carbon price database (August 2025)") +
  theme(legend.position=c(0.05,0.8),
        axis.text = element_blank(),
        axis.title = element_blank())+
  guides(alpha='none')

gg1


gg2<-ggplot(world_map,aes(fill=100*cp_var_rel, map_id=region, alpha=zero)) +
  geom_map(map=world_map) +
  scale_fill_viridis_c() +
  scale_alpha_manual(values=c(1,0.1)) +
  expand_limits(x = world_map$long, y = world_map$lat) +
  coord_map("moll") +
  theme_bw() +
  labs(title="Relative difference in carbon prices 2024",
       subtitle = "(Highest price - ecp) / highest price",
       fill="%",
       caption="Emissions-weighted carbon price database (August 2025)") +
  theme(legend.position=c(0.05,0.8),
        axis.text = element_blank(),
        axis.title = element_blank())+
  guides(alpha='none')

gg2


gg3<-ggplot(world_map,aes(fill=cp_var_abs, map_id=region, alpha=zero)) +
  geom_map(map=world_map) +
  scale_fill_viridis_c() +
  scale_alpha_manual(values=c(1,0.1)) +
  expand_limits(x = world_map$long, y = world_map$lat) +
  coord_map("moll") +
  theme_bw() +
  labs(title="Highest carbon price minus emissions-weighted average 2024",
       fill="USD",
       caption="Emissions-weighted carbon price database (August 2025)") +
  theme(legend.position=c(0.05,0.8),
        axis.text = element_blank(),
        axis.title = element_blank())+
  guides(alpha='none')

gg3


ggsave(gg1,filename=paste0("ecp_map",".svg"),
       device="svg",
       height=5,
       width=10,
       path=file.path(here::here(),"_output","_figures","plots"))

ggsave(gg2,filename=paste0("ecp_var_rel_map",".svg"),
       device="svg",
       height=5,
       width=10,
       path=file.path(here::here(),"_output","_figures","plots"))

ggsave(gg3,filename=paste0("ecp_var_abs_map",".svg"),
       device="svg",
       height=5,
       width=10,
       path=file.path(here::here(),"_output","_figures","plots"))



