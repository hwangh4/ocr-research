# Author: Scarlett Hwang
# OCR Text-image File Conversion Script
# January 10th, 2020

# convert -density 200 Hládek2017_Article_LearningStringDistanceWithSmoo.pdf test1.png
# for i in *.pdf ; do
#   name=${i%.*}
#   png=$name.png
#   convert -density 200 "$i" "$png" ;
#   tesseract "$png" "test_$name" ;
# done

#!/bin/bash

# if ! [ -d output ]; then
#   mkdir output
# fi

# For every .txt file within r_string_diff folder
for filename in *.txt ; do
  # Extract just the name of the file without extention
  jpg=${filename%.txt}
  # Convert .txt to .jpg (ONLY FIRST PAGE WORKS) and export
  /Applications/LibreOffice.app/Contents/MacOS/soffice --convert-to jpg "$filename"
  # Do OCR on the created .jpg file and export
  tesseract $jpg.jpg "$jpg-converted"

  # echo ${filename%.*}
  # echo $jpg
  # echo `<$jpg`
  # /Applications/LibreOffice.app/Contents/MacOS/soffice --headless --norestore --writer --convert-to jpg "$filename"
  #/Applications/LibreOffice.app/Contents/MacOS/soffice --convert-to jpg "$filename"
  #tesseract $jpg.jpg "$jpg-converted"
done
