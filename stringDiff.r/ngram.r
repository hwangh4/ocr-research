## Author: Scarlett Hwang
## Eviction OCR Research 
## June 25th, 2019

library(readr)
library(dplyr)

## main 1, read in files 
# dir <- list.files(pattern="*.txt")
# v <- NULL
# for (i in 1:length(dir)) {
#   word_ngram(read_file(dir[i]), 2)
# }

## main 2, compare two files' probabilities
orig_table <- word_ngram(read_file("text1.txt"), 2)
ocr_table <- word_ngram(read_file("text2.txt"), 2) #HERE compare needed

## word n-gram 
## passes every occurance to chart maker function
## params: sentence - the sentence we want to analyze
##         num - number of n-gram (2 for bigram)
word_ngram <- function(sentence, num) {
  # remove new lines
  sentence <- stringr::str_replace(sentence, '\n', ' ')
  # tokenize words
  text <- strsplit(sentence, ' ') %>% Reduce(c, .)
  ngram <- c()

  for (x in 1:length(text)) {
    if (nchar(text[x]) < 2)
      next
    splitted <- c(strsplit(text[x], ''))[[1]] #substring instead
    for (letter in 1:(length(splitted)-1)) {
      ngram <- append(ngram, paste0(splitted[seq(letter, letter+num-1)], collapse = ""))
    }
  }
  freq_list(c(ngram))
}

## make frequency list
## recieve every occurance from word_ngram function and create a named vector list
## params: ngram - bigram pairs of passed text file
freq_list <- function(ngram) {
  # set start number (0) to all unique bigrams
  return(table(ngram))
  #print(prop.table(table(ngram)))
}


