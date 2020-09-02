library(tidyverse)  
library(rvest)    
library(stringr)
library(stringi)
library(rebus)
library(dplyr)
library(purrr)
#library(lubridate)

################
#OCENY REZYSEROW
################

url <- 'http://www.filmweb.pl/ranking/person/director'

#Ile stron ma dany ranking
get_last_page <- function(html){
  pages_data <- html %>% 
    html_nodes('.pagination__link') %>% 
    html_text()                   
  
  #Bez ostatniego, bo wczytuje strzalke
  pages_data[(length(pages_data)-1)] %>%            
    unname() %>%                                     
    as.numeric()                                     
}

#Pozyskanie nazw rezyserow
nazwy_rezyserow <- function(html){
  html %>% 
    html_nodes('.person__name') %>% 
    html_text() %>% 
    str_trim() %>% 
    unlist()
}

#Pozyskanie ocen rezyserow
oceny <- function(html){
  html %>% 
    html_nodes('.rate__value') %>% 
    html_text() %>% 
    str_trim() %>% 
    unlist()
}

#Tworzenie ramki danych dla rezyserow
get_data_table <- function(html){

  rezyser <- nazwy_rezyserow(html)
  ocena <- oceny(html)

  min_length <- min(length(rezyser), length(ocena))
  
  combined_data <- tibble(Rezyser = rezyser[1:min_length],
                          Ocena_rezysera = ocena[1:min_length])
  combined_data <- as.data.frame(combined_data)
}

#Pobieranie danych z linku
get_data_from_url <- function(url){
  html <- read_html(url)
  get_data_table(html)
}

#Funkcja wykonujaca wszystkie zaimplementowane wyzej funkcje, zapisujaca wynik do postaci tsv
scrape_write_table <- function(url){
  first_page <- read_html(url)
  latest_page_number <- get_last_page(first_page)
  list_of_pages <- str_c(url, '?page=', 1:latest_page_number)
  
  list_of_pages %>% 
    map(get_data_from_url) %>%  
    bind_rows() %>% 
    readr::write_tsv('rezyserzy.tsv')
}

rezyserzy <- scrape_write_table(url)
View(rezyserzy)

##############
#OCENY AKTOROW
##############

url2 <- 'http://www.filmweb.pl/ranking/person/actors/male'

nazwy_aktorow <- function(html){
  html %>% 
    html_nodes('.film__link') %>% 
    html_text() %>% 
    str_trim() %>% 
    unlist()
}

get_data_table <- function(html){
  aktor <- nazwy_rezyserow(html)
  ocena <- oceny(html)
  
  min_length <- min(length(aktor), length(ocena))
  
  combined_data <- tibble(Aktor = aktor[1:min_length],
                          Ocena_aktora = ocena[1:min_length])
  combined_data <- as.data.frame(combined_data)
}

scrape_write_table <- function(url){
  first_page <- read_html(url)
  latest_page_number <- get_last_page(first_page)
  #Ustawiono recznie na 20, ze wzgledu na problem z przewijalnoscia paska
  list_of_pages <- str_c(url, '?page=', 1:20)
  
  list_of_pages %>% 
    map(get_data_from_url) %>%
    bind_rows() %>%
    readr::write_tsv('aktorzy.tsv')
}

aktorzy <- scrape_write_table(url2)


#Usuwanie numeracji aktorow
for (c in 1:length(aktorzy$Aktor)){
  aktorzy$Aktor[c] <- gsub("\\d","",aktorzy$Aktor[c])
  aktorzy$Aktor[c] <- substring(aktorzy$Aktor[c],2)
}
View(aktorzy)

##############
#OCENY AKTOREK
##############

url3 <- 'http://www.filmweb.pl/ranking/person/actors/female'

get_data_table <- function(html){
  
  aktor <- nazwy_rezyserow(html)
  ocena <- oceny(html)
  
  min_length <- min(length(aktor), length(ocena))
  
  combined_data <- tibble(Aktor = aktor[1:min_length],
                          Ocena_aktorki = ocena[1:min_length])
  combined_data <- as.data.frame(combined_data)
}

scrape_write_table <- function(url){
  first_page <- read_html(url)
  latest_page_number <- get_last_page(first_page)
  #Ustawiono recznie na 15, ze wzgledu na problem z przewijalnoscia paska
  list_of_pages <- str_c(url, '?page=', 1:15)
  
  list_of_pages %>% 
    map(get_data_from_url) %>%
    bind_rows() %>%
    readr::write_tsv('rezyserzy.tsv')
}

aktorki <- scrape_write_table(url3)

#Usuwanie numeracji aktorek
for (c in 1:length(aktorki$Aktor)){
  aktorki$Aktor[c] <- gsub("\\d","",aktorki$Aktor[c])
  aktorki$Aktor[c] <- substring(aktorki$Aktor[c],2)
}
View(aktorki)

######################
#BAZA IMDB + REZYSERZY
######################

imdb <- read.csv(file="C:/Users/Jan/Desktop/imdb_filmy.csv",sep=",",dec=".",header = TRUE, stringsAsFactors = FALSE)

#Usuniecie niepotrzebnych kolumn
imdb$Rank <- NULL
imdb$Description <- NULL
imdb$Metascore <- NULL
imdb$Year <- NULL

#Wybranie glownego aktora
for (c in 1:length(imdb$Actors)){
  imdb[c,4] <- gsub(",.*", '', imdb[c,4])
}

colnames(imdb) <- c("Tytul","Gatunek","Rezyser","Aktor","Dlugosc","Ocena","Glosy","Box office")

#Dolaczanie rezyserow
nowa <- merge(x = imdb, y = rezyserzy, by="Rezyser", all = FALSE)

#Zamiana znakow dziesietnych
for (c in 1:length(nowa$Ocena_rezysera)){
  nowa[c,9] <- gsub(',', '.', nowa[c,9])
}
for (c in 1:length(aktorzy$Ocena_aktora)){
  aktorzy[c,2] <- gsub(',', '.', aktorzy[c,2])
}
for (c in 1:length(aktorki$Ocena_aktorki)){
  aktorki[c,2] <- gsub(',', '.', aktorki[c,2])
}

nowa$Ocena_rezysera <- as.numeric(nowa$Ocena_rezysera)
aktorzy$Ocena_aktora <- as.numeric(aktorzy$Ocena_aktora)
aktorki$Ocena_aktorki <- as.numeric(aktorki$Ocena_aktorki)

write.csv(nowa, file="C:/Users/Jan/Desktop/nowa.csv",sep='\t',dec='.')
write.csv(aktorzy, file="C:/Users/Jan/Desktop/aktorzy.csv",sep='\t',dec='.')
write.csv(aktorki, file="C:/Users/Jan/Desktop/aktorki.csv",sep='\t',dec='.')

#########################
#NOWA + AKTORZY + AKTORKI
#########################

nowa$X <- NULL
aktorzy$X <- NULL
aktorki$X <- NULL

aktorzy$Aktor <- as.character(aktorzy$Aktor)
nowa$Aktor <- as.character(nowa$Aktor)
aktorki$Aktor <- as.character(aktorki$Aktor)

#Poprawianie niepotrzebnych stringow
for (c in 1:length(aktorzy$Aktor)){
  aktorzy[c,1] <- gsub('^ ', '',aktorzy[c,1])
}
for (c in 1:length(aktorki$Aktor)){
  aktorki[c,1] <- gsub('^ ', '',aktorki[c,1])
}
colnames(aktorki) <- c("Aktor","Ocena_aktora")

#Laczenie ramek danych
tabela2 <- merge(nowa,aktorzy,by="Aktor")
tabela3 <- merge(nowa,aktorki,by="Aktor")

tabelka <- rbind(tabela2,tabela3)
View(tabelka)

#Uzupelnianie brakujacych wartosci
tabelka[31,8] <- 180.56
tabelka[59,8] <- 31.13
tabelka[68,8] <- 286.14
tabelka[68,8] <- 4.04

#Ostateczny zbior danych
write.csv(tabelka, file="C:/Users/Jan/Desktop/filmy.csv",sep='\t',dec='.')