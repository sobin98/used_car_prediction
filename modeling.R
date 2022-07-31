used_car<-read.csv("cars_processed.csv")
library(dplyr)
#기존모델
reg<-lm(가격~주행거리+연료+연식+배기량+옵션_선루프+옵션_열선앞+옵션_열선뒤+옵션_전방센서+옵션_후방센서+옵션_전방캠+옵션_후방캠+옵션_어라운드뷰+옵션_네비순정+소유자변경횟수+사고상세_전손+사고상세_침수분손+보험_내차피해.횟수.+보험_내차피해.가격.+사고상세_타차가해.횟수.+보험_타차피해.가격.,data=used_car)

#더미변수로 바꾸는 코드
install.packages("mltools")
library(mltools)
library(data.table)

used_car$색상<-as.factor(used_car$색상)
used_car$연료<-as.factor(used_car$연료)

newdata<-one_hot(as.data.table(used_car))

#개선된모델
regnewdata<-lm(신차대비가격~주행거리+연료_0+연료_1+연료_2+ +연식+ 배기량+색상_0+색상_1+색상_2+색상_3+색상_4+색상_5+옵션_선루프+옵션_열선앞+옵션_열선뒤+옵션_전방센서+옵션_후방센서+옵션_전방캠+옵션_후방캠+옵션_어라운드뷰+옵션_네비순정+소유자변경횟수+사고상세_전손+사고상세_침수분손+보험_내차피해.횟수.+보험_내차피해.가격.+사고상세_타차가해.횟수.+보험_타차피해.가격.,data=newdata)

#stepwise 사용
regnewdata<-lm(신차대비가격~주행거리+연료_0+연료_1+연료_2+배기량+색상_0+색상_1+색상_2+색상_3+색상_4+색상_5+옵션_선루프+옵션_열선앞+옵션_열선뒤+옵션_전방센서+옵션_후방센서+옵션_전방캠+옵션_후방캠+옵션_어라운드뷰+옵션_네비순정+소유자변경횟수+사고상세_전손+사고상세_침수분손+보험_내차피해.횟수.+보험_내차피해.가격.+사고상세_타차가해.횟수.+보험_타차피해.가격.,data=newdata)


#전진선택법
forward<-step(regnewdata,direction = "forward")
summary(forward)
#후진선택법
backward<-step(regnewdata,direction = "backward")
summary(backward)
#단계적선택법
stepwise<-step(regnewdata,direction = "both")
summary(stepwise)

library(gridExtra)
library(olsrr)
library(ggrepel)
Row<-c(1:559)
re.dat<-cbind(1:559,newdata[,])
res.influence.dat<-cbind(re.dat,cooks.distance(backward),dffits(backward),ols_hadi(backward)$hadi)
colnames(res.influence.dat)[c(40,41,42)]<-c("C_i","DFITs_i","H_i")
p2<-ols_plot_dffits(backward)
p3<-ggplot(res.influence.dat,aes(x=Row,y=H_i))+geom_point()+geom_text_repel(data = filter(res.influence.dat, H_i>0.2),aes(label=Row))
grid.arrange(p2,p3,nrow=1) 

tmp<-newdata[-c(101,106,226,233,248,287,300,321,339,362,376,390,478),]
tmp1<-lm(신차대비가격 ~ 주행거리 + 연료_0 + 연식 + 
                 배기량 + 색상_1 + 색상_2 + 색상_3 + 옵션_선루프 + 
                 옵션_열선앞 + 옵션_전방센서 + 옵션_후방캠 + 
                 옵션_어라운드뷰 + 옵션_네비순정 + 소유자변경횟수 + 보험_내차피해.가격. + 
                 보험_타차피해.가격., data = tmp)
summary(tmp1)
plot(backward,2)
plot(tmp1,2)

ggplot(tmp,aes(x=주행거리,y=신차대비가격))+
  geom_point()+
  geom_smooth(method=lm,se=F)+xlab("distance driven")+ylab("price ratio")
ggplot(tmp,aes(x=주행거리,y=log(신차대비가격)))+
  geom_point()+
  geom_smooth(method=lm,se=F)+xlab("distance driven")+ylab("price ratio")

ggplot(tmp,aes(x=연식,y=신차대비가격))+
  geom_point()+
  geom_smooth(method=lm,se=F)+xlab("year")+ylab("price ratio")
ggplot(tmp,aes(x=연식,y=log(신차대비가격)))+
  geom_point()+
  geom_smooth(method=lm,se=F)+xlab("year")+ylab("price ratio")

ggplot(tmp,aes(x=보험_내차피해.가격.,y=신차대비가격))+
  geom_point()+
  geom_smooth(method=lm,se=F)+xlab("car damage price (mine)")+ylab("price ratio")
s1_dam1<-data.frame(damp1=tmp$보험_내차피해.가격.,priceratio=tmp$신차대비가격)
s4lm<-lm(priceratio~damp1,data=s1_dam1)
summary(s4lm)
s1_dam1$damp1<-ifelse(s1_dam1$damp1==0,1,s1_dam1$damp1)
s1_dam1$Y_new<-s1_dam1$priceratio/s1_dam1$damp1
s1_dam1$X_new<-1/s1_dam1$damp1
lm_dam1<-lm(Y_new~X_new,data=s1_dam1)
summary(lm_dam1)
ggplot(s1_dam1,aes(x=X_new,y=Y_new))+
  geom_point()+
  geom_smooth(method=lm,se=F)+xlab("car damage price (mine)")+ylab("price ratio")

ggplot(tmp,aes(x=보험_타차피해.가격.,y=신차대비가격))+
  geom_point()+
  geom_smooth(method=lm,se=F)+xlab("car damage price (others)")+ylab("price ratio")
s1_dam2<-data.frame(damp2=tmp$보험_타차피해.가격.,priceratio=tmp$신차대비가격)
s5lm<-lm(priceratio~damp2,data=s1_dam2)
summary(s5lm)
s1_dam2$damp2<-ifelse(s1_dam2$damp2==0,1,s1_dam2$damp2)
s1_dam2$Y_new<-s1_dam2$priceratio/s1_dam2$damp2
s1_dam2$X_new<-1/s1_dam2$damp2
lm_dam2<-lm(Y_new~X_new,data=s1_dam2)
summary(lm_dam2)
ggplot(s1_dam2,aes(x=X_new,y=Y_new))+
  geom_point()+
  geom_smooth(method=lm,se=F)+xlab("car damage price (others)")+ylab("price ratio")

datatrv<-data.frame(tmp[,-c(8,36,34,32)])
damp2tmp<-ifelse(tmp$보험_타차피해.가격.==0,1,tmp$보험_타차피해.가격.)
datatrv$신차대비가격<-tmp$신차대비가격/damp2tmp
datatrv$사고상세_타차가해.가격.<-1/damp2tmp
damp1tmp<-ifelse(tmp$보험_내차피해.가격.==0,1,tmp$보험_내차피해.가격.)
datatrv$사고상세_내차피해.가격.<-1/damp1tmp
datatrv$배기량<-1/tmp$배기량
names(datatrv)
datatr<-lm(log(신차대비가격)~주행거리 + 연료_0 + 연식 + 
             배기량 + 색상_1 + 색상_2 + 색상_3 + 옵션_선루프 + 
             옵션_열선앞 + 옵션_전방센서 + 옵션_후방캠 + 
             옵션_어라운드뷰 + 옵션_네비순정 + 소유자변경횟수 + 사고상세_내차피해.가격. + 
             사고상세_타차가해.가격.,data=datatrv)
summary(datatr)

tmp3<-lm(신차대비가격 ~ log(주행거리) + 연료_0 + log(연식) + 
                 배기량 + 색상_1 + 색상_2 + 색상_3 + 옵션_선루프 + 
                 옵션_열선앞 + 옵션_전방센서 + 옵션_후방캠 + 
                 옵션_어라운드뷰 + 옵션_네비순정 + 소유자변경횟수 + 보험_내차피해.가격. + 
                 보험_타차피해.가격., data = tmp)
summary(tmp3)