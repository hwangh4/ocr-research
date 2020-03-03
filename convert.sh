# Author: Scarlett Hwang
# OCR Text-image File Conversion Script
# January 10th, 2020

if [ $USER == "siim" ]; then
    SOFFICE=$(which soffice)
    # note: soffice program must not be running on background!
    MAGICK=convert
else
    SOFFICE=/Applications/LibreOffice.app/Contents/MacOS/soffice
    MAGICK=magick
fi

LINES=50  # lines per page

while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
      -i|--input)
  	FILE="$2"
  	shift # past argument
  	shift # past value
      ;;
      -h|--help)
  	echo "usage: $0 -i inputfile"
  	echo "  -l <n> : put n lines per page"
  	exit 0
  	;;
      -l|--lines)
  	LINES="$2"
  	shift # past argument
  	shift # past value
      ;;
      -p|--preserve)
    PRESERVE=1
    shift # past argument
      ;;
      *)    # unknown option
      POSITIONAL+=("$1") # save it in an array for later
      shift # past argument
      ;;
  esac
done

basename=${FILE%.*}
if [ "$basename" == "" ]; then
    echo "please specify the input file"
    exit 1
fi
split -l $LINES $FILE "${basename}-chunk-" || exit 2
# use digits to distinguish chunks, put 25 lines per page

for subfile in ${basename}-chunk-* ; do
    echo $subfile
    # Extract just the name of the file without extention

    # Convert .txt to .jpg (ONLY FIRST PAGE WORKS) and export
    $SOFFICE --convert-to jpg $subfile

    # # Add dither
    $MAGICK $subfile.jpg -dither Riemersma -colors 2 $subfile-dithered.jpg
    #
    # # Do OCR on the created .jpg file and export
    tesseract $subfile-dithered.jpg "$subfile-converted"
    if [ "$PRESERVE" != 1 ]; then
      rm $subfile.jpg $subfile-dithered.jpg
    fi
done
