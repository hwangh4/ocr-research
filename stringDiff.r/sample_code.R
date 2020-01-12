  with open('nalgae.txt', 'r', encoding='utf-8', newline='\n') as f:
  file = f.read()
  sample_file = ''.join(file)
  
  #어절 n-gram 분석
  #sentence: 분석할 문장, num_gram: n-gram 단위
  def word_ngram(sentence, num_gram):
    # in the case a file is given, remove escape characters
    sentence = sentence.replace('\n', ' ').replace('\r', ' ')
  text = tuple(sentence.split(' '))
  ngrams = [text[x:x+num_gram] for x in range(0, len(text))]
  return tuple(ngrams)
  
  #음절 n-gram 분석
  #sentence: 분석할 문장, num_gram: n-gram 단위
  def phoneme_ngram(sentence, num_gram):
    text = tuple(sentence) # split the sentence into an array of characters
  ngrams = [text[x:x+num_gram] for x in range(0, len(text))]
  return ngrams
  
  #n-gram 빈도 리스트 생성
  def make_freqlist(ngrams):
    freqlist = {}
  
  for ngram in ngrams:
    if (ngram in freqlist):
    freqlist[ngram] += 1
  else:
    freqlist[ngram] = 1
  
  return freqlist
  
  ngrams = word_ngram(sample_file, 3)
  freqlist = make_freqlist(ngrams)
  sorted_freqlist = sorted(freqlist.items(), key=operator.itemgetter(1))
  print(sorted_freqlist)
  
  dummy <-data.frame("letter", "freq")
  colnames(dummy) <- c("letter", "freq")
  for(i in 0:10) {
    if ("b" %in% dummy) {
      dummy <- cbind("a", 1)
    } else {
      dummy <- c("b", 2)
    }
  }
  
  library(purrr)
  
  