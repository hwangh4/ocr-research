## Scarlett Hwang
## OCR Error Correction Research

## This file reads in the original text file and the converted file to compare the differences.


# Read in original and converted text files, return vector returned form
# string difference function
# param: input file text1 - input file name of original text file
#        input file text2 - input file name of OCR-ed text file
readFiles <- function(text1="text1.txt", text2="text2.txt") {
  original <- read_file(text1) # does this have to be a full path?
  converted <- read_file(text2) # does this have to be a full path?
  return(stringDiff(original, converted))
}

# Read in original and converted files' texts, splice them into word-level
# vectors, compare each indices, and return the different words.
# param: string original - string of original text file contents
#        string converted - string of converted text file contents
stringDiff <- function(original, converted) {
  origVec <- unlist(strsplit(original, split=" "))
  convertVec <- unlist(strsplit(converted, split=" "))
  output <- c()
  
  origi = 0
  convi = 0
  for (i in 1:length(origVec)) {
    origi <- origi + 1
    convi <- convi + 1
    orig <- origVec[origi]
    conv <- convertVec[convi]
    if (orig != conv) {
      splitted_orig <- strsplit(orig, "")
      splitted_conv <- strsplit(conv, "")
      # in case where srting length is diff
      if (length(splitted_orig[[1]]) != length(splitted_conv[[1]])) {
        print("JEeh")
      }
      
      output <- c(output, origVec[origi], convertVec[convi]) 
    }
  }
  return(output)
}

# below runs function aboves
# print(readFiles("text1.txt", "text2.txt"))

originals <- list.files(myfolder, pattern = "orig")

for(files in list.files(myfolder)) {
  
}
