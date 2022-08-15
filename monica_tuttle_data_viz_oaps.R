################################################################################
                              
                              # IMPORT DATA 
#===============================================================================
library(tidyverse)

#RColorBrewer::display.brewer.all()

dataset <- read.csv("C:\\OneDrive - Allegheny County\\Documents\\R\\oaps.csv")

allegations <- read.csv("C:\\OneDrive - Allegheny County\\Documents\\R\\allegations.csv")

reasons_not_closed_20_days <- read.csv("C:\\OneDrive - Allegheny County\\Documents\\R\\not_in_20_days.csv")

oaps <- select(dataset, CLIENT_ID, START_DATE, invest_is_complete_date_d, 
               provider_name_cleaned, initial_invest_or_reassessment, 
               allegations_by_reporter_new, substantiated_new, difference_in_days, 
               why_no_determ_in_20_days_new, case_close_reason_new, reassessments, 
               substantiated_or_unsubstantiated)

################################################################################

                              # FILTER IMPORTED DATA
#===============================================================================

oaps_remove_no_diff_in_days_calculated <- filter(oaps, difference_in_days != "")

reasons_not_closed_20_days_ignore <- filter(reasons_not_closed_20_days,
                                            why_no_determ_in_20_days_d != "Awaiting financial records - APS only" &
                                            why_no_determ_in_20_days_d != "Unable to locate consumer")

reasons_not_closed_ignore_abandonment <- filter(reasons_not_closed_20_days_ignore,
                                                allegations_by_reporter_d != "Abandonment")                                    
                                    
################################################################################

                              # VISUALIZE DATA
#===============================================================================

# Case count by agency
ggplot(oaps_remove_no_diff_in_days_calculated, aes(provider_name_cleaned, fill = provider_name_cleaned)) +
  geom_bar() +
  geom_text(aes(label = ..count..), stat = "count", vjust = 1.5, colour = "white") +
  labs(x = "agency", title = "CASE COUNT by Agency", subtitle = paste("N = ", count(oaps_remove_no_diff_in_days_calculated))) +
  theme(plot.title = element_text(color = "#6A5ACD", face = "bold", size = 20), legend.position = "none", 
        axis.title.x = element_text(color = "#6A5ACD", face = "bold"), axis.title.y = element_text(color = "#6A5ACD", face = "bold"))

# Comparing the average amount of days to complete investigations by agency 

eval(substitute(ggplot(aes(x = provider_name_cleaned, y = difference_in_days, 
    fill = provider_name_cleaned), 
    data = oaps_remove_no_diff_in_days_calculated) +
    stat_summary(fun = median, geom = "bar") +
    stat_summary(aes(label=round(..y..)), fun = median, geom = "text", size = 4, 
        hjust = 2, colour = "white") + 
    coord_flip(ylim = c(0, 70)) +
    #coord_cartesian(ylim = c(0, 70)) +
    labs(x = "agency", y = "median days", fill = "agency", 
      title = "Days to Complete Investigations by Agency - MEDIAN",
      subtitle = paste("N = ", count(oaps_remove_no_diff_in_days_calculated))) +
      theme(plot.title = element_text(color = "#6A5ACD", face = "bold", size = 20), 
            axis.title.x = element_text(color = "#6A5ACD", face = "bold"), axis.title.y = element_text(color = "#6A5ACD", face = "bold"))))

eval(substitute(ggplot(aes(x = provider_name_cleaned, y = difference_in_days, 
    fill = provider_name_cleaned), data = oaps_remove_no_diff_in_days_calculated) +
    stat_summary(fun = mean, geom = "bar") +
    stat_summary(aes(label=round(..y..)), fun = mean, 
      geom = "text", size = 4, hjust = 2, colour = "white") +
      coord_flip(ylim = c(0, 70)) +
      labs(x = "agency", y = "average days", fill = "agency", 
      title = "Days to Complete Investigations by Agency - MEAN (average)",
      subtitle = paste("N = ", count(oaps_remove_no_diff_in_days_calculated))) +
      theme(plot.title = element_text(color = "#6A5ACD", face = "bold", size = 20), 
            axis.title.x = element_text(color = "#6A5ACD", face = "bold"), axis.title.y = element_text(color = "#6A5ACD", face = "bold")))) 
      

#===============================================================================

# Case count of investigations by allegation type

ggplot(allegations, aes(allegations_by_reporter, 
  fill = allegations_by_reporter)) +
  geom_bar() +
  geom_text(aes(label = ..count..), stat = "count", vjust = 0, colour = "black") +
  labs(x = "allegation type", title = "CASE COUNT - Allegation Type", 
    subtitle = paste("N = ", count(allegations))) +
  scale_fill_brewer(palette = "Spectral") +  
  theme(legend.position = "none") +
  theme(axis.text.x = element_text(angle = 30, hjust = 1)) +
  theme(plot.title = element_text(color = "#6A5ACD", face = "bold", size = 20), legend.position = "none", 
        axis.title.x = element_text(color = "#6A5ACD", face = "bold"), axis.title.y = element_text(color = "#6A5ACD", face = "bold")) 


# Comparing the average amount of days to complete investigations by allegation type 

eval(substitute(ggplot(aes(x = allegations_by_reporter, y = difference_in_days, 
  fill = allegations_by_reporter), data = allegations) +
  stat_summary(fun = median, geom = "bar") +
  coord_flip(ylim = c(0, 60)) +
  stat_summary(aes(label=round(..y..)), fun = median, geom = "text", size = 4, 
                hjust = 1.5) +
  labs(x = "allegation type", y = "median days", fill = "allegation type", 
    title = "Days to Complete Investigations by Allegation Type - MEDIAN",
    subtitle = paste("N = ", count(allegations))) +
  scale_fill_brewer(palette = "Spectral"))) +
  theme(plot.title = element_text(color = "#6A5ACD", face = "bold", size = 20), 
        axis.title.x = element_text(color = "#6A5ACD", face = "bold"), axis.title.y = element_text(color = "#6A5ACD", face = "bold")) 


eval(substitute(ggplot(aes(x = allegations_by_reporter, y = difference_in_days, 
  fill = allegations_by_reporter), 
  data = allegations) +
  coord_flip() +
  stat_summary(fun = mean, geom = "bar") +
  stat_summary(aes(label=round(..y..)), fun = mean, geom = "text", size = 4, 
               hjust = 1.5) +
  labs(x = "allegation type", y = "average days", fill = "allegation type", 
    title = "Days to Complete Investigations by Allegation Type - MEAN (average)",
    subtitle = paste("N = ", count(allegations))) +
  scale_fill_brewer(palette = "Spectral"))) +
  theme(plot.title = element_text(color = "#6A5ACD", face = "bold", size = 20),
        axis.title.x = element_text(color = "#6A5ACD", face = "bold"), axis.title.y = element_text(color = "#6A5ACD", face = "bold"))


#===============================================================================

# Measures of center and spread shown through box and whisker plots, broken down
# by agency and allegation type

ggplot(allegations, aes(difference_in_days, 
  allegations_by_reporter, 
  fill = factor(provider_name_cleaned))) +
  geom_boxplot(outlier.shape = NA) + # removing outliers
  coord_cartesian(xlim = c(0, 200)) +
  labs(x = "days", y = "allegation type", fill = "agency", 
       title = "Duration of Investigations by Agency and Allegation Type",
       subtitle = paste("N = ", count(allegations))) +
  theme(plot.title = element_text(color = "#6A5ACD", face = "bold", size = 14),
        axis.title.x = element_text(color = "#6A5ACD", face = "bold"), axis.title.y = element_text(color = "#6A5ACD", face = "bold"))


ggplot(allegations, aes(difference_in_days, 
      allegations_by_reporter, fill = factor(provider_name_cleaned))) +
      geom_boxplot(outlier.size = .7) +
      labs(x = "days", y = "allegation type", fill = "agency", 
        title = "Duration of Investigations by Agency and Allegation Type",
        subtitle = paste("N = ", count(allegations))) +
  theme(plot.title = element_text(color = "#6A5ACD", face = "bold", size = 14), 
        axis.title.x = element_text(color = "#6A5ACD", face = "bold"), axis.title.y = element_text(color = "#6A5ACD", face = "bold")) 


#===============================================================================

# Count of records with reasons identified for why a case wasn't closed in 20 days
# broken down by allegation type

ggplot(reasons_not_closed_ignore_abandonment, aes(why_no_determ_in_20_days_d, 
  fill = allegations_by_reporter_d)) +
  geom_bar(position = "dodge") +
  coord_flip() +
  labs(x = "reasons", fill = "allegation", 
    title = "Reasons for not closing cases within 20 days - by Allegation Type",
    subtitle = paste("N = ", count(reasons_not_closed_ignore_abandonment))) +
  scale_fill_brewer(palette = "Spectral") +
  theme(plot.title = element_text(color = "#6A5ACD", face = "bold", size = 14), 
        axis.title.x = element_text(color = "#6A5ACD", face = "bold"), axis.title.y = element_text(color = "#6A5ACD", face = "bold")) 


# Count of records with reasons identified for why a case wasn't closed in 20 days
# broken down by agency

ggplot(reasons_not_closed_ignore_abandonment, aes(why_no_determ_in_20_days_d, 
  fill = provider_name_cleaned)) +
  geom_bar(position = "dodge") +
  coord_flip() +
  labs(x = "reasons", fill = "agency", 
    title = "Reasons for not closing cases within 20 days - by Agency",
    subtitle = paste("N = ", count(reasons_not_closed_ignore_abandonment))) +
  theme(plot.title = element_text(color = "#6A5ACD", face = "bold", size = 14), 
        axis.title.x = element_text(color = "#6A5ACD", face = "bold"), axis.title.y = element_text(color = "#6A5ACD", face = "bold")) 

#===============================================================================
# Sandbox
oaps %>%
  ggplot( aes(x = provider_name_cleaned, y = difference_in_days, 
              fill = provider_name_cleaned)) +
  coord_flip() +
  geom_boxplot(outlier.size = .6) +
  geom_jitter(color="black", size=.6, alpha=0.9) +
  theme(
    legend.position="none",
    plot.title = element_text(size=11)
  ) +
  ggtitle("Duration of Investigations by Agency") +
  xlab("agency") +
  ylab("days")

eval(substitute(ggplot(aes(x = why_no_determ_in_20_days_d, y = difference_in_days, 
                           fill = allegations_by_reporter_d), 
                       data = reasons_not_closed_ignore_abandonment) +
                  stat_summary(fun = median, geom = "bar", position = "dodge") +
                  #coord_cartesian(ylim = c(0, )) +
                  coord_flip() +
                  scale_fill_brewer(palette = "RdPu") + 
                  labs(x = "reason", y = "median days", fill = "allegation", 
                       title = "Median Days",
                       subtitle = paste("N = ", count(reasons_not_closed_ignore_abandonment))))) 

eval(substitute(ggplot(aes(x = why_no_determ_in_20_days_d, y = difference_in_days, 
                           fill = provider_name_cleaned), 
                       data = reasons_not_closed_ignore_abandonment) +
                  stat_summary(fun = median, geom = "bar", position = "dodge") +
                  #coord_cartesian(ylim = c(0, )) +
                  coord_flip() +
                  labs(x = "agency", y = "median days", fill = "agency", 
                       title = "Median Days",
                       subtitle = paste("N = ", count(reasons_not_closed_ignore_abandonment))))) 

