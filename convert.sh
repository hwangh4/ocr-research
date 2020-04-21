# Author: Scarlett Hwang
# OCR Text-image File Conversion Script
# January 10th, 2020

if [ $USER == "AndyLee"] ; then
    MAGICK=magick
else
    MAGICK=convert
fi

POSITIONAL=()
LINES=50  # lines per page
FORCE=""  # don't overwrite the folder
POINTSIZE=12  # how bit a font to use

while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
      -f|--force)
	  echo "forcing the directory to be overwritten"
	  FORCE=1
	  shift
	  ;;
      -h|--help)
  	  echo "usage: $0 [-l n] <inputfile.txt>"
	  echo "split the inputfile into page images, add noise, convert back"
	  echo "the results will be put in the directory named <inputfile>"
	  echo "  -f : force the output dir to be overwritten"
  	  echo "  -l <n> : put n lines per page (default 50)"
	  echo "  -p : keep the image files"
	  echo "  --pointsize : font size in points (default 12)"
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
      --pointsize)
	  POINTSIZE="$2"
	  shift
	  shift
	  ;;
      *)    # unknown option
      POSITIONAL+=("$1") # save it in an array for later
      shift # past argument
      ;;
  esac
done

echo "  pointsize ${POINTSIZE} (change with --pointsize)"
file=${POSITIONAL[0]}
basename=$([[ "$file" = *.* ]] && echo "${file%.*}" || echo "${file}")
if [ -z "$basename" ]; then
    echo "please specify the input file"
    exit 1
fi

echo "splitting $file into chunks of $LINES lines"
if [ -d $basename ]; then
    if [ -z $FORCE ]; then
	echo "cannot proceed -- directory ${basename} exists"
	echo "use --force to overwrite"
	exit 1
    fi
    echo "cleaning ${basename}"
    rm -rf $basename/*
else
    mkdir $basename || exit 1
fi
cd $basename

split -l $LINES ../$file "${basename}-chunk-" || exit 2

## rename chunks back to .txt so it is easier to handle this afterwards
for subfile in ${basename}-chunk-* ; do
    mv $subfile $subfile.txt
done

## main conversion loop
n=$(ls ${basename}-chunk-*.txt|wc -l)
i=1
for subfile in ${basename}-chunk-*.txt ; do
    echo " -- "$subfile "($i/$n)"
    # Extract just the name of the file without extention
    subbase=${subfile%.txt}

    ## Convert text to jpg
    ## Play with font and point size
    ## Uses "annotate", intended for adding text to images
    convert -size 3000x2000 xc:white -pointsize $POINTSIZE\
	    -fill black\
	    -annotate +15+15 "@$subfile"\
	    -trim -bordercolor "#FFF" -border 20 +repage\
	    ${subbase}.jpg

    # Add dither
    $MAGICK $subbase.jpg -dither Riemersma -colors 2 $subbase-dithered.jpg

    # Do OCR on the created .jpg file and export
    tesseract $subbase-dithered.jpg "$subbase-converted"

    # Preserve jpeg files if specified
    if [ "$PRESERVE" != 1 ]; then
      rm $subbase.jpg $subbase-dithered.jpg
    fi
    i=$((i + 1))
done
