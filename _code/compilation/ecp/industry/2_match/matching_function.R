#### Matching function for ecp

calculate_ewcp<-function(yr,
                         ctry,
                         sect,
                         ecp_data,
                         gloria_q_data,
                         concordance,
                         type) 
{
  # This function is written for easy debugging
  
  ### Step 1: Create calculation dataframe
  df<-as.data.frame(matrix(NA,nrow=nrow(concordance),ncol=2))
  colnames(df)<-c("Sat_ind","cp")
  df$Sat_ind<-concordance$Sat_ind
  # the below is to make the function work for both industry satellites z 
  # and demand satellites y
  if(type=="z"){
    sectorf<-paste(ctry,sect,sep=".")
  } else if(type=="y"){
    sectorf=ctry
  }
  
  ### Step 2: Extract ecp data
  de<-ecp_data%>%filter(jurisdiction == ctry)
  de<-de%>%filter(year == yr)
  
  ### Step 3: Extract gloria satellites data
  # keep only EDGAR CO2 accounts excl short cycle
  zqs<-gloria_q_data
  zqs<-zqs %>% filter (grepl("co2",Sat_indicator))
  zqs<-zqs %>% filter (grepl("excl_short_cycle",Sat_indicator))
  # keep only ctry of interest
  zqs <- zqs %>% select(c(Sat_indicator,contains(ctry)))
  # shorten the strings in the sat indicator to keep only ipcc code
  zqs <- zqs %>% mutate(Sat_indicator = substr(Sat_indicator,29,nchar(Sat_indicator)-18))
  # keep only sector of interest
  if(type=="z"){
    zqs <- zqs %>% select (c(Sat_indicator,sectorf))
    # rename colnames
    zqs <- zqs %>% rename(emissions = sectorf)
  } else if(type=="y"){
    # rename colnames
    colnames(zqs)[2]<-"emissions"
  }
  # add to df
  df['emissions']<-zqs$emissions
  
  ### Step 4: Import concordance between ipcc sectors in ECP and in GLORIA
  i_c_p <- concordance %>% pivot_longer(-Sat_ind,names_to="cp_ind",values_to="ident")
  
  ### Step 5: Map carbon price data from ECP to GLORIA EDGAR categories
  # this is an aggregation from 76 categories to 73 categories
  for(i in 2:nrow(df)){
    # extract names of the ECP categories that correspond to GLORIA EDGAR categories
    tmpnms1<-vector()
    tmpnms2<-vector()
    tmpnms3<-vector()
    tmpnms1<-i_c_p$cp_ind[i_c_p$ident==1 & i_c_p$Sat_ind==df$Sat_ind[i]]
    tmpnms2<-i_c_p$cp_ind[i_c_p$ident==2 & i_c_p$Sat_ind==df$Sat_ind[i]]
    tmpnms3<-i_c_p$cp_ind[i_c_p$ident==3 & i_c_p$Sat_ind==df$Sat_ind[i]]
    if(length(tmpnms1==1)){ # if there is unique concordance then use that
      df$cp[i]<-de$ecp_all_usd[de$ipcc_code==tmpnms1]
    } else if (length(tmpnms2==1)){ # if we only have a lower resolution ecp, use that (e.g. 1A1C price for 1A1ci emissions)
      df$cp[i]<-de$ecp_all_usd[de$ipcc_code==tmpnms2]
    } else if (length(tmpnms3)>0){ # if we only have a higher resolution ecp, then use the emissions-weighted average
      tmpvectp<-vector()
      # extract the carbon price data for the subcategories
      tmpvectc<-vector()
      for(j in 1:length(tmpnms3)){
        tmpvectp[j]<-de$ecp_all_usd[de$ipcc_code==tmpnms3[j]]
        tmpvectc[j]<-de$CO2[de$ipcc_code==tmpnms3[j]]
      }
      if(sum(tmpvectc)>0){ # if there are any emissions
        df$cp[i]<-sum((tmpvectc*tmpvectp)/sum(tmpvectc)) # compute emissions-weighted average
      } else {
        df$cp[i]<-0 # in case there are no emissions, we assume zero (otherwise division by zero generates NA)
      }
    } else {} # otherwise e.g. in case of 5B, where we have no conc, do nothing
  }
  
  ### Step 6: Rename 5 digit codes
  df$Sat_ind[df$Sat_ind=="1A1ci"]<-"1A1c1"
  df$Sat_ind[df$Sat_ind=="1A1cii"]<-"1A1c2"
  df$Sat_ind[df$Sat_ind=="1A4ci"]<-"1A4c1"
  df$Sat_ind[df$Sat_ind=="1A4cii"]<-"1A4c2"
  df$Sat_ind[df$Sat_ind=="1A4ciii"]<-"1A4c3"
  
  ### Step 7: Calculate emissions-weighted average carbon price for missing cases
  # we identify the applicable carbon price for each category with emissions
  # this step is only there for special cases (1A2, 1A3b, 3C1). If these categories
  # have no price, but subcategories do, then we calculate the emissions-weighted
  # average across subcategories and use the result.
  df['acp']<-NA
  for(i in 1:nrow(df)){
    # find all subcategories
    tmpnms<-vector()
    tmpnms<-df[startsWith(df$Sat_ind, df$Sat_ind[i]),1]
    tmpnms<-tmpnms[-1] # keep only subcategories
    # get prices for those subcategories
    tmpvectp<-df$cp[df$Sat_ind %in% tmpnms]
    # get carbon for those subcategories
    tmpvectc<-df$emissions[df$Sat_ind %in% tmpnms]
    # if the main category has no aggregate price, but subcategories do,
    # we use the emissions-weighted average price across subcategories
    if (df$cp[i] == 0 & sum(tmpvectp) > 0) {
      df$acp[i] <- sum(tmpvectp*tmpvectc)/sum(tmpvectc)
    } else { # otherwise we use the price of the main category (it might be 0)
      df$acp[i] <- df$cp[i]
    }
  }
  
  ### Step 8: Calculate overall emissions-weighted carbon price for the sector
  # divide categorical emissions by total
  df['relem']<-df$emissions/df$emissions[df$Sat_ind=="total"]
  # if we have zero total emissions this introduces NAs. Change those cases to zero
  # df$relem[is.na(df$relem)]<-0
  # multiply relative emissions by categorical prices
  df['relcc']<-df$relem*df$acp
  df$relcc[df$Sat_ind=="total"]<-0
  # result is the sum of all categorical weighted prices
  result<-sum(df$relcc)
  
  ### Step 9: Return result
  return(result)
}


# vector of categories covered by eu ets II
eu_ets_ipcc_II <- c("1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A",
                    "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H",
                    "1A2I", "1A2J", "1A2K", "1A2L", "1A2M", "1A3A2",
                    "1C1A", "1C2B",
                    "2A1", "2A2", "2A3", "2A4A", "2B1", "2B2", "2B3", 
                    "2B4", "2B5", "2B6", "2B7", "2B8F",
                    "2C1", "2C2", "2C3", "2C4", "2C5", "2C6", "2H1")


ets2_coverage_fun<-function(yr,
                           ctry,
                           sect,
                           gloria_q_data,
                           concordance,
                           type){
  
  ### Step 1: Create calculation dataframe
  df<-as.data.frame(matrix(NA,nrow=nrow(concordance),ncol=2))
  colnames(df)<-c("Sat_ind","ets2cover")
  df$Sat_ind<-concordance$Sat_ind
  # the below is to make the function work for both industry satellites z 
  # and demand satellites y
  if(type=="z"){
    sectorf<-paste(ctry,sect,sep=".")
  } else if(type=="y"){
    sectorf=ctry
  }
  
  ### Step 2: Extract gloria satellites data
  # keep only EDGAR CO2 accounts excl short cycle
  zqs<-gloria_q_data
  zqs<-zqs %>% filter (grepl("co2",Sat_indicator))
  zqs<-zqs %>% filter (grepl("excl_short_cycle",Sat_indicator))
  # keep only ctry of interest
  zqs <- zqs %>% select(c(Sat_indicator,contains(ctry)))
  # shorten the strings in the sat indicator to keep only ipcc code
  zqs <- zqs %>% mutate(Sat_indicator = substr(Sat_indicator,29,nchar(Sat_indicator)-18))
  # keep only sector of interest
  if(type=="z"){
    zqs <- zqs %>% select (c(Sat_indicator,sectorf))
    # rename colnames
    zqs <- zqs %>% rename(emissions = sectorf)
  } else if(type=="y"){
    # rename colnames
    colnames(zqs)[2]<-"emissions"
  }
  # add to df
  df['emissions']<-zqs$emissions
  
  ### Step 3: Import concordance between ipcc sectors in ECP and in GLORIA
  i_c_p <- concordance %>% pivot_longer(-Sat_ind,names_to="cp_ind",values_to="ident")
  
  ### Step 4: Map ets II coverage from ECP to GLORIA EDGAR categories
  # We define all categories from 1A1 to 1A2 as covered by EU ETS 2
  # These are energy related emissions from energy industries and from manufacturing
  df$ets2cover[which(df$Sat_ind=="1A1a"):which(df$Sat_ind=="1A2m")]<-1
  # Road transportation is not covered
  df$ets2cover[which(df$Sat_ind=="1A3b"):which(df$Sat_ind=="1A3b_RES")]<-0
  # special case: aviation 1A3a (only domestic 1A3aii is covered)
  # we use CO2 emissions from the ecp dataset as allocation key 
  df$ets2cover[df$Sat_ind=="1A3a"]<-
    ecp$CO2[
      ecp$jurisdiction==tmpc & ecp$year==yr & ecp$ipcc_code=="1A3A2"]/
    ecp$CO2[
      ecp$jurisdiction==tmpc & ecp$year==yr & ecp$ipcc_code=="1A3A"]
  # Other energy related emissions (like fugitive emissions) are not covered
  df$ets2cover[which(df$Sat_ind=="1A3c"):which(df$Sat_ind=="1B2")]<-0
  # We define all categories from 2A1 to 2A3 as covered by EU ETS2
  # These are process emissions from the main mineral industries (cement, lime, glass)
  df$ets2cover[which(df$Sat_ind=="2A1"):which(df$Sat_ind=="2A3")]<-1
  # special case: other process uses of carbonates 2A4 (only Ceramics 2A4a is covered)
  # Given that ecp does not differentiate between subsectors here, we just assume
  # that the whole 2A4 category is covered
  df$ets2cover[which(df$Sat_ind=="2A4")]<-1
  # Process emissions from chemical ind and metal ind (2B:2C) (we cover them all)
  df$ets2cover[which(df$Sat_ind=="2B"):which(df$Sat_ind=="2C")]<-1
  # Process emissions from other industries (2D:2G) not covered
  df$ets2cover[which(df$Sat_ind=="2D"):which(df$Sat_ind=="2G")]<-0
  # special case: 2H only 2H1 pulp and paper industry covered
  # we account for this in our gloria sector specific ecp mapping, so can use the
  # concordance table here. Sawmill pulp paper sector is identified by the case 
  # where 2H2 does not map onto 2H
  if(i_c_p$ident[i_c_p$cp_ind=="2H2" & i_c_p$Sat_ind=="2H"]==0){
    df$ets2cover[which(df$Sat_ind=="2H")]<-1
  } else {
    df$ets2cover[which(df$Sat_ind=="2H")]<-0
  }
  # All else not covered
  df$ets2cover[which(df$Sat_ind=="3A1"):which(df$Sat_ind=="5A")]<-0
  
  ### Step 5: calculate the extent to which the gloria sector is covered by ets2
  df['emissions_covered']<-df$ets2cover*df$emissions
  result<-sum(df$emissions_covered,na.rm=T)/df$emissions[df$Sat_ind=="total"]
  
  ### Step 6: Return result
  return(result)
}






