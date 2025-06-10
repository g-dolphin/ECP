################################################################################
##### checkplots ###############################################################
################################################################################


### Setup

library(dplyr)
library(ggplot2)

if(cbase=="edgar" & pl=="cons_p"){
  dfz<-read.csv(file.path(here::here(),
                          "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                          "constantPrice","FixedXRate",
                          "ecp_gloria_edgar_industry_CO2.csv"))
  dfz$ecp_edgar[is.na(dfz$ecp_edgar)]<-0
  dfz <- dfz %>% rename(ecp=ecp_edgar)
  dfz <- dfz %>% rename(co2_total = co2_edgar_total)
  dfy<-read.csv(file.path(here::here(),
                          "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                          "constantPrice","FixedXRate",
                          "ecp_gloria_edgar_finaldem_CO2.csv"))
  dfy$ecp_edgar[is.na(dfy$ecp_edgar)]<-0
  dfy <- dfy %>% rename(ecp=ecp_edgar)
  dfy <- dfy %>% rename(co2_total = co2_edgar_total)
  dfy <- dfy %>% filter(sector == "Household final consumption P.3h")
} else if (cbase=="oecd" & pl =="cons_p"){
  dfz<-read.csv(file.path(here::here(),
                          "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                          "constantPrice","FixedXRate",
                          "ecp_gloria_oecd_industry_CO2.csv"))
  dfz$ecp_oecd[is.na(dfz$ecp_oecd)]<-0
  dfz <- dfz %>% rename(ecp=ecp_oecd)
  dfz <- dfz %>% rename(co2_total = co2_oecd_total)
  dfy<-read.csv(file.path(here::here(),
                          "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                          "constantPrice","FixedXRate",
                          "ecp_gloria_oecd_finaldem_CO2.csv"))
  dfy$ecp_oecd[is.na(dfy$ecp_oecd)]<-0
  dfy <- dfy %>% rename(ecp=ecp_oecd)
  dfy <- dfy %>% rename(co2_total = co2_oecd_total)
  dfy <- dfy %>% filter(sector == "Household final consumption P.3h")
} else if(cbase=="edgar" & pl=="curr_p"){
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
} else if (cbase=="oecd" & pl=="curr_p"){
  dfz<-read.csv(file.path(here::here(),
                          "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                          "currentPrice","FlexXRate",
                          "ecp_gloria_oecd_industry_CO2.csv"))
  dfz$ecp_oecd[is.na(dfz$ecp_oecd)]<-0
  dfz <- dfz %>% rename(ecp=ecp_oecd)
  dfz <- dfz %>% rename(co2_total = co2_oecd_total)
  dfy<-read.csv(file.path(here::here(),
                          "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                          "currentPrice","FlexXRate",
                          "ecp_gloria_oecd_finaldem_CO2.csv"))
  dfy$ecp_oecd[is.na(dfy$ecp_oecd)]<-0
  dfy <- dfy %>% rename(ecp=ecp_oecd)
  dfy <- dfy %>% rename(co2_total = co2_oecd_total)
  dfy <- dfy %>% filter(sector == "Household final consumption P.3h")
}

# remove the extra co2 columns not needed here
if(cbase=="edgar"){
  dfy <- dfy %>% select(-c(co2_edgar_1a3b,co2_edgar_1a4))
} else if (cbase=="oecd"){
  dfy <- dfy %>% select(-c(co2_oecd_1a3b,co2_oecd_1a4))
}



df<-rbind(dfz,dfy)
df <- df %>% select(year,country,sector,ecp,co2_total)
rm(dfz,dfy)


################################################################################
### individual specific plots 
################################################################################


# ctrs<-c("Germany","France","Italy")
# sctrs<-c("Electric power generation, transmission and distribution")
# sctrs<-c("Road transport")
# 
# ggplot(df %>% filter(country %in% ctrs,sector %in% sctrs,year != 2022),
#        aes(x=year,y=ecp_edgar,colour=country_sector)) +
#   geom_line() +
#   geom_hline(yintercept=0,linetype="dashed",colour="black")+
#   ylab("USD / tCO2")+
#   labs(title="Emissions-weighted carbon prices over time",
#        subtitle=paste("Based on WCPD",pl,"price and GLORIA",cbase,"emission keys",sep=" "))+
#   theme_classic()+
#   theme(legend.position="bottom",legend.title=element_blank())+
#   guides(colour=guide_legend(ncol=1))
#   
# rm(ctrs,sctrs)

################################################################################
### prep plots #########################################################
################################################################################


unlink(file.path(wd,"3_checks",pl,cbase),recursive = T)
dir.create(file.path(wd,"3_checks",pl,cbase))



################################################################################
### make country plots #########################################################
################################################################################
dir.create(file.path(wd,"3_checks",pl,cbase,"by_country"))
dir.create(file.path(wd,"3_checks",pl,cbase,"by_country","cross_sector"))

sq<-unique(df$sector)
cq<-unique(df$country)
yrs<-unique(df$year)

# ok then we put this into a loop

for(i in 1:length(yrs)){
  yr<-yrs[i]
  print(paste("plotting",yr,"ecp"))
  dfi<-filter(df,year==yr)
  dir.create(file.path(wd,"3_checks",pl,cbase,"by_country","cross_sector",yr))
  for(j in 1:length(cq)){
    ctry<-cq[j]
    dfic<-filter(dfi,country==ctry)
    if(sum(dfic$ecp)==0){} else{
      dfic$sector<-factor(dfic$sector, levels = rev(dfic$sector))
      if(ctry=="CSSR/Czech Republic (1990/1991)"){ctryn<-"Czech Republic"}else{ctryn<-ctry}
      gg<-ggplot(dfic,aes(x=sector,y=ecp)) +
        geom_bar(stat='identity',fill="dodgerblue4") +
        geom_hline(yintercept = sum(dfic$ecp*dfic$co2_total)/sum(dfic$co2_total), linetype="dashed",colour="red")+
        coord_flip() +
        labs(title = paste("Post-match industry ecp",ctryn,yr,sep=" "),
             subtitle = paste("National ecp:",round(sum(dfic$ecp*dfic$co2_total)/sum(dfic$co2_total),digits = 2),"USD/tCO2",pl,sep=" "),
             caption = paste("Emissions-weighted carbon prices database",Sys.Date(),sep=" ")) +
        theme_bw()+
        theme(axis.title = element_blank(),
              axis.text.y = element_text(size=rel(0.8)))
      ggsave(gg,filename=paste0("ecp_",yr,"_",ctryn,".svg"),
             device="svg",
             height=10,
             width=10,
             path=file.path(wd,"3_checks",pl,cbase,"by_country","cross_sector",yr))
      rm(gg,ctryn)
    }
    rm(ctry,dfic)
  }
  rm(yr,dfi)
}
rm(i,j)

################################################################################
### make sector plots #########################################################
################################################################################

dir.create(file.path(wd,"3_checks",pl,cbase,"by_sector"))
dir.create(file.path(wd,"3_checks",pl,cbase,"by_sector","cross_country"))

sq<-unique(df$sector)
cq<-unique(df$country)
yrs<-unique(df$year)

for(i in 1:length(yrs)){
  yr<-yrs[i]
  print(paste("plotting",yr,"ecp"))
  dfi<-filter(df,year==yr)
  dir.create(file.path(wd,"3_checks",pl,cbase,"by_sector","cross_country",yr))
  for(j in 1:length(sq)){
    sect<-sq[j]
    dfic<-filter(dfi,sector==sect)
    if(sum(dfic$ecp)==0){} else{
      dfic<-filter(dfic,ecp!=0)
      sectn<-substr(sect,start=1,stop=20)
      gg<-ggplot(dfic,aes(x=reorder(country,-ecp),y=ecp)) +
        geom_bar(position="dodge",stat='identity',fill="dodgerblue4") +
        labs(title = paste("Post-match industry ecp",substr(sect,start=1,stop=20),yr,sep=" "),
             subtitle = paste("USD/tCO2",pl,sep=" "),
             caption = paste("Emissions-weighted carbon prices database",Sys.Date(),sep=" ")) +
        theme_bw()+
        theme(axis.title = element_blank(),
              axis.text.x = element_text(angle=45,hjust=1,vjust=1))
      ggsave(gg,filename=paste0("ecp_",yr,"_",j,".svg"),
             device="svg",
             height=5,
             width=10,
             path=file.path(wd,"3_checks",pl,cbase,"by_sector","cross_country",yr))
      rm(gg,sectn)
    }
    rm(sect,dfic)
  }
  rm(yr,dfi)
}


################################################################################
rm(list=ls()[! ls() %in% c("wd","pl","gversion","cbase")])
