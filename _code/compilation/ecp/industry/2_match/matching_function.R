#### Matching function for ecp

calculate_ewcp<-function(yr,
                         ctry,
                         sect,
                         ecp_data,
                         gloria_q_data,
                         concordance,
                         type,
                         sourcedat) 
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
  # keep only OECD / EDGAR
  zqs<-gloria_q_data
  zqs<-zqs %>% filter (grepl("co2",Sat_indicator))
  zqs<-zqs %>% filter (grepl(sourcedat,Sat_indicator))
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




