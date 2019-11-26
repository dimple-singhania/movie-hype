## get search index############
### generated file.
keywords=c("jolie")
time=("2019-10-18 2019-11-13")
trends = gtrends(keywords,time = time )
#select only interst over time 
time_trend=trends$interest_over_time
time_trend
plot<-ggplot(data=time_trend, aes(x=date, y=hits,group=keyword,col=keyword))+
  geom_line()+xlab('Time')+ylab('Relative Interest')+ theme_bw()+
  theme(legend.title = element_blank(),legend.position="bottom",legend.text=element_text(size=12))+ggtitle("Google Search Volume")
plot
out = data.frame(time_trend)
out
write.csv(out,"mal_keywrod.csv", row.names = FALSE)
write.table(out,file = 'mal_keywrod',sep = ',',row.names = FALSE)## file name is here.
### after you have the file, only flip the date and search index.
#############the model with keyword
library("zoo")
library("forecast")
### if you could read the file but can't read the number, change it manually in the excel: $313,111 -> 313111
hit = mal_hit[2]
hitts = ts(hit, start =1,frequency =1)
sale = Mal_sale[2]
salets = ts(sale, start =1,frequency =1)
plot(salets)
traing = salets[1:12]
test = salets[13:25]
traing_lof = log(traing)
plot(log(salets))
total_diff = diff(traing_lof,differences = 1)##
plot(ts(total_diff), ylab = 'the log of sales')
#adf.test(total_diff)
acf(total_diff)## accordin to the acf score, only 1 time difference is enough for the model.
arimafit=arima(traing_lof,order=c(1,1,7),xreg = hitts[1:12])#1,1,7: 1 for 1 time difference, 1 for related to past 1 actual data, 7 for 7 past residual linear combo.
#arimaModel_1=arima(traing_lof, order=c(0,1,2))
#arimaModel_2=arima(traing_lof, order=c(1,1,0))
#arimaModel_3=arima(traing_lof, order=c(1,1,2))
### tried several parameter and several days, found out 10 days would be best to get the result.
## look at the parameters
pred = predict(arimafit,newxreg=hitts[13:20])## 20 days is the max, otherwise the model is off.
par(mfrow = c(1,1))
plot(traing_lof,type='l',xlim=c(1,50),ylim = c(13,17))
lines(pred$pred,col='red')
lines(log(salets),col='blue')
accuracy(arimafit)
