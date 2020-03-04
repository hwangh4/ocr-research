# Author: Scarlett Hwang
# OCR Text-image File Conversion Script
# January 10th, 2020

if [ $USER == "siim" ] || [ $USER == "otoomet" ] ; then
    echo "Ott"
    SOFFICE=$(which soffice)
    # note: soffice program must not be running on background!
    MAGICK=convert
else
    echo "Scarlett"
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

echo "splitting $FILE into chunks of $LINES lines"

split -l $LINES $FILE "${basename}-chunk-" || exit 2
# use digits to distinguish chunks, put 25 lines per page

for subfile in ${basename}-chunk-* ; do
    echo $subfile
    # Extract just the name of the file without extention

    ## Convert text to jpg
    ## Play with font and point size
    ## Uses "annotate", intended for adding text to images
    convert -size 3000x2000 xc:white -pointsize 12\
	    -fill black\
	    -annotate +15+15 "@$subfile"\
	    -trim -bordercolor "#FFF" -border 20 +repage\
	    $subfile.jpg

    # Add dither
    $MAGICK $subfile.jpg -dither Riemersma -colors 2 $subfile-dithered.jpg

    # Do OCR on the created .jpg file and export
    tesseract $subfile-dithered.jpg "$subfile-converted"

    # Preserve jpeg files if specified
    if [ "$PRESERVE" != 1 ]; then
      rm $subfile.jpg $subfile-dithered.jpg
    fi
done
