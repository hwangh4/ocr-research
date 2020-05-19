# ocr-research

UW iSchool Eviction Study - Optical Character Recognition Research

Optical character recognition (OCR) is a widely used method to extract texts for page images. While modern software can convert high-quality images of printed text virtually flawlessly, small text, low-quality image or background noise still cause noticeable problems. In particular, the OCR software is often confusing letters or letter combinations that look similar, e.g. “in” for “m” or “t” for “i”. While ordinary fuzzy string matching is based on assumptions that all characters are equally likely to be swapped, this is clearly not the case OCR errors.
We develop a method to automatically correct OCR-retrieved texts using a Bayesian approach. We proceed in two steps: first, we convert a large corpus of texts into images, add dithering noise and convert the images back to text using tesseract OCR software. Thereafter we compare the original and the converted texts and tabulate the resulting character errors and the character bigram errors. The error tables are converted to Bayesian error probabilities. Second, the final error correction proceeds by computing the probability the observed word in OCR-retrieved text corresponds to a known word in a large corpus of English texts, based on the probabilities calculated in the first step. We report the performance of our algorithm as a function of font type, font size, and noise intensity. Both tools, the text conversion and error tabulation, and the final error correction, are released on Github.
This method contributes to devising faster, more reliable, and more context-sensitive automatic analysis of a printed text, such as processing of large quantities of photocopies of official documents that often come in uneven quality.

## Code:

### convert.sh

bash script to convert text file into images, add noise, and OCR the
result back to text.  Accepts bz2-compressed files.  Various options,
including number of lines per page, font size, and whether to preserve
the images.

### More Information
#### Lightning Talk
https://www.youtube.com/watch?v=FIiYrQxCz9A
