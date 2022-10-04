################################################################################

# Author: Monica Tuttle
# Topic: Older Adult Protective Services Data Visualizations
# Updated 9/2/22

################################################################################
                              
                              # STEP ONE - IMPORT DATA 
#===============================================================================
library(tidyverse)

dataset <- read.csv("[INSERT FILE PATH].oaps.csv")

allegations <- read.csv("[INSERT FILE PATH].allegations.csv")

reasons_not_closed_20_days <- read.csv("[INSERT FILE PATH].not_in_20_days.csv")

oaps <- select(dataset, CLIENT_ID, START_DATE, invest_is_complete_date_d, 
               provider_name_cleaned, initial_invest_or_reassessment, 
               allegations_by_reporter_new, substantiated_new, difference_in_days, 
               why_no_determ_in_20_days_new, case_close_reason_new, reassessments, 
               substantiated_or_unsubstantiated)

################################################################################

                              # STEP TWO - FILTER IMPORTED DATA
#===============================================================================

oaps_remove_no_diff_in_days_calculated <- filter(oaps, difference_in_days != "")

reasons_not_closed_20_days_ignore <- filter(reasons_not_closed_20_days,
                                            why_no_determ_in_20_days_d != "Awaiting financial records - APS only" &
                                            why_no_determ_in_20_days_d != "Unable to locate consumer")

reasons_not_closed_ignore_abandonment <- filter(reasons_not_closed_20_days_ignore,
                                                allegations_by_reporter_d != "Abandonment")                                    
                                    
################################################################################

                              # STEP THREE - VISUALIZE DATA
#===============================================================================

# Case count by agency
ggplot(oaps_remove_no_diff_in_days_calculated, aes(fct_rev(fct_infreq(provider_name_cleaned)), fill = provider_name_cleaned)) +
  geom_bar() +
  geom_text(aes(label = ..count..), stat = "count", vjust = 1.5, colour = "white", size = 7) +
  labs(x = "agency", y = "count", title = "Case Count by Agency", subtitle = paste("n = ", count(oaps_remove_no_diff_in_days_calculated))) +
  theme(plot.title = element_text(color = "#6A5ACD", face = "bold", size = 22), plot.subtitle = element_text(size = 18), legend.position = "none", 
        axis.title.x = element_text(color = "#6A5ACD", face = "bold", size = 18), axis.title.y = element_text(color = "#6A5ACD", face = "bold", size = 18),
        axis.text = element_text(size = 16))

# Comparing the average amount of days to complete investigations by agency 

eval(substitute(ggplot(aes(x = reorder(provider_name_cleaned, -difference_in_days), y = difference_in_days, 
    fill = provider_name_cleaned), 
    data = oaps_remove_no_diff_in_days_calculated) +
    stat_summary(fun = median, geom = "bar") +
    stat_summary(aes(label=round(..y..)), fun = median, geom = "text", size = 6, 
        hjust = 2, colour = "white") + 
    coord_flip(ylim = c(0, 70)) +
    labs(x = "agency", y = "median days", fill = "agency", 
    title = "MEDIAN Days to Complete Investigations by Agency",
    subtitle = paste("n = ", count(oaps_remove_no_diff_in_days_calculated))) +
    theme(legend.position = "none", plot.title = element_text(color = "#6A5ACD", face = "bold", size = 22), plot.subtitle = element_text(size = 18), 
          axis.title.x = element_text(color = "#6A5ACD", face = "bold", size = 18), axis.title.y = element_text(color = "#6A5ACD", face = "bold", size = 18),
          axis.text = element_text(size = 16))))

eval(substitute(ggplot(aes(x = reorder(provider_name_cleaned, -difference_in_days), y = difference_in_days, 
    fill = provider_name_cleaned), data = oaps_remove_no_diff_in_days_calculated) +
    stat_summary(fun = mean, geom = "bar") +
    stat_summary(aes(label=round(..y..)), fun = mean, 
    geom = "text", size = 6, hjust = 2, colour = "white") +
    coord_flip(ylim = c(0, 70)) +
    labs(x = "agency", y = "average days", fill = "agency", 
    title = "AVERAGE Days to Complete Investigations by Agency",
    subtitle = paste("n = ", count(oaps_remove_no_diff_in_days_calculated))) +
    theme(legend.position = "none", plot.title = element_text(color = "#6A5ACD", face = "bold", size = 22), plot.subtitle = element_text(size = 18),
          axis.title.x = element_text(color = "#6A5ACD", face = "bold", size = 18), axis.title.y = element_text(color = "#6A5ACD", face = "bold", size = 18), 
          axis.text = element_text(size = 16))))

#===============================================================================

# Case count of investigations by allegation type

ggplot(allegations, aes(fct_rev(fct_infreq(allegations_by_reporter)), 
  fill = allegations_by_reporter)) +
  geom_bar() +
  geom_text(aes(label = ..count..), stat = "count", vjust = 0, colour = "black", size = 6) +
  labs(x = "allegation type", title = "Case Count by Allegation Type", 
    subtitle = paste("n = ", count(allegations))) +
  scale_fill_brewer(palette = "Spectral") +  
  theme(legend.position = "none") +
  theme(axis.text.x = element_text(angle = 20, hjust = 1)) +
  theme(plot.title = element_text(color = "#6A5ACD", face = "bold", size = 22), legend.position = "none", plot.subtitle = element_text(size = 18),
        axis.title.x = element_text(color = "#6A5ACD", face = "bold", size = 18), axis.title.y = element_text(color = "#6A5ACD", face = "bold", size = 18), 
        axis.text = element_text(size = 16))

# Comparing the average amount of days to complete investigations by allegation type 

eval(substitute(ggplot(aes(x = reorder(allegations_by_reporter, -difference_in_days), y = difference_in_days, 
  fill = allegations_by_reporter), data = allegations) +
  stat_summary(fun = median, geom = "bar") +
  coord_flip(ylim = c(0, 60)) +
  stat_summary(aes(label=round(..y..)), fun = median, geom = "text", size = 6, 
                hjust = 1.5) +
  labs(x = "allegation type", y = "median days", fill = "allegation type", 
    title = "MEDIAN Days to Complete Investigations by Allegation Type",
    subtitle = paste("n = ", count(allegations))) +
  scale_fill_brewer(palette = "Spectral"))) +
  theme(legend.position = "none", plot.title = element_text(color = "#6A5ACD", face = "bold", size = 22), plot.subtitle = element_text(size = 18), 
        axis.title.x = element_text(color = "#6A5ACD", face = "bold", size = 18), axis.title.y = element_text(color = "#6A5ACD", face = "bold", size = 18),
        axis.text = element_text(size = 16)) 


eval(substitute(ggplot( aes(x = reorder(allegations_by_reporter, -difference_in_days), y = difference_in_days, 
  fill = allegations_by_reporter), 
  data = allegations) +
  coord_flip() +
  stat_summary(fun = mean, geom = "bar") +
  stat_summary(aes(label=round(..y..)), fun = mean, geom = "text", size = 6, 
               hjust = 1.5) +
  labs(x = "allegation type", y = "average days", fill = "allegation type", 
    title = "AVERAGE Days to Complete Investigations by Allegation Type",
    subtitle = paste("n = ", count(allegations))) +
  scale_fill_brewer(palette = "Spectral"))) +
  theme(legend.position = "none", plot.title = element_text(color = "#6A5ACD", face = "bold", size = 22), plot.subtitle = element_text(size = 18),
        axis.title.x = element_text(color = "#6A5ACD", face = "bold", size = 18), axis.title.y = element_text(color = "#6A5ACD", face = "bold", size = 18),
        axis.text = element_text(size = 16))


#===============================================================================

# Measures of center and spread shown through box and whisker plots, broken down
# by agency and allegation type

ggplot(allegations, aes(difference_in_days, 
  fct_rev(fct_infreq(allegations_by_reporter)), 
  fill = factor(provider_name_cleaned))) +
  geom_boxplot(outlier.shape = NA) + # removing outliers
  coord_cartesian(xlim = c(0, 200)) +
  labs(x = "days", y = "allegation type", fill = "agency", 
       title = "Duration of Investigations by Agency and Allegation Type",
       subtitle = paste("n = ", count(allegations))) +
  theme(plot.title = element_text(color = "#6A5ACD", face = "bold", size = 22), plot.subtitle = element_text(size = 18),
        axis.title.x = element_text(color = "#6A5ACD", face = "bold", size = 18), axis.title.y = element_text(color = "#6A5ACD", face = "bold", size = 18),
        axis.text = element_text(size = 16))


ggplot(allegations, aes(difference_in_days, 
      fct_rev(fct_infreq(allegations_by_reporter)), fill = factor(provider_name_cleaned))) +
      geom_boxplot(outlier.size = 1) +
      labs(x = "days", y = "allegation type", fill = "agency", 
        title = "Duration of Investigations by Agency and Allegation Type",
        subtitle = paste("n = ", count(allegations))) +
      theme(plot.title = element_text(color = "#6A5ACD", face = "bold", size = 22), plot.subtitle = element_text(size = 18),
        axis.title.x = element_text(color = "#6A5ACD", face = "bold", size = 18), axis.title.y = element_text(color = "#6A5ACD", face = "bold", size = 18),
        axis.text = element_text(size = 16)) 


#===============================================================================

# Count of records with reasons identified for why a case wasn't closed in 20 days
# broken down by allegation type

ggplot(reasons_not_closed_ignore_abandonment, aes(fct_rev(fct_infreq(why_no_determ_in_20_days_d)), 
  fill = allegations_by_reporter_d)) +
  geom_bar(position = "dodge") +
  coord_flip() +
  labs(x = "reasons", fill = "allegation", 
    title = "Reasons for not closing cases within 20 days - by Allegation Type",
    subtitle = paste("n = ", count(reasons_not_closed_ignore_abandonment))) +
  scale_fill_brewer(palette = "Spectral") +
  theme(plot.title = element_text(color = "#6A5ACD", face = "bold", size = 18), plot.subtitle = element_text(size = 16),
        axis.title.x = element_text(color = "#6A5ACD", face = "bold", size = 16), axis.title.y = element_text(color = "#6A5ACD", face = "bold", size = 16),
        axis.text = element_text(size = 14))


# Count of records with reasons identified for why a case wasn't closed in 20 days
# broken down by agency

ggplot(reasons_not_closed_ignore_abandonment, aes(fct_rev(fct_infreq(why_no_determ_in_20_days_d)), 
  fill = provider_name_cleaned)) +
  geom_bar(position = "dodge") +
  coord_flip() +
  labs(x = "reasons", fill = "agency", 
    title = "Reasons for not closing cases within 20 days - by Agency",
    subtitle = paste("n = ", count(reasons_not_closed_ignore_abandonment))) +
  theme(plot.title = element_text(color = "#6A5ACD", face = "bold", size = 18), plot.subtitle = element_text(size = 16), 
        axis.title.x = element_text(color = "#6A5ACD", face = "bold", size = 16), axis.title.y = element_text(color = "#6A5ACD", face = "bold", size = 16),
        axis.text = element_text(size = 14)) 
