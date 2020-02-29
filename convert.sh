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

case $1 in
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
    -i|--input)
	LINES="$2"
	shift # past argument
	shift # past value
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac

basename=${FILE%.*}
split -d -l 50 $FILE "${basename}-chunk-"
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
done
