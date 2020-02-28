# Author: Scarlett Hwang
# OCR Text-image File Conversion Script
# January 10th, 2020

# For every .txt file within r_string_diff folder
for filename in *.txt ; do
  # if splitting a file needed, use code below
  split $filename file
done

for subfile in file* ; do

    # Extract just the name of the file without extention
    name=$subfile

    # Convert .txt to .jpg (ONLY FIRST PAGE WORKS) and export
    /Applications/LibreOffice.app/Contents/MacOS/soffice --convert-to jpg $name $name

    # # Add dither
    magick $name.jpg -dither Riemersma -colors 2 $name-dithered.jpg
    #
    # # Do OCR on the created .jpg file and export
    tesseract $name-dithered.jpg "$name-converted"
done
