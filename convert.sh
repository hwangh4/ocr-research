# Author: Scarlett Hwang
# OCR Text-image File Conversion Script
# January 10th, 2020

if [ $USER == "AndyLee" ] ; then
    MAGICK=magick
else
    MAGICK=convert
fi

POSITIONAL=()
SPLITLINES=50  # lines per page (LINES interferes with screen?)
FORCE=""  # don't overwrite the folder
POINTSIZE=12  # how bit a font to use
MAXPAGES=1000000000  # at most process 1G pages
FONT="Helvetica"

while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
      -f|--force)
	  echo "forcing the directory to be overwritten"
	  FORCE=1
	  shift
	  ;;
      --font)
  	  FONT="$2"
  	  shift # past argument
  	  shift # past value
	  ;;
      -h|--help)
  	  echo "usage: $0 [-l n] <inputfile.txt>"
	  echo "split the inputfile into page images, add noise, convert back"
	  echo "the results will be put in the directory named <inputfile>"
	  echo "accepts input file in .bz2 compressed format"
	  echo "  -f, --force     : force the output dir to be overwritten"
  	  echo "  -l <n>, --lines : put n lines per page (default 50)"
	  echo "  -p, --preserve  : preserve the image files"
	  echo "  --pointsize     : font size in points (default 12)"
  	  exit 0
  	  ;;
      -l|--lines)
  	  SPLITLINES="$2"
  	  shift # past argument
  	  shift # past value
	  ;;
      -m|--max-pages)
  	  MAXPAGES="$2"
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

echo "  pointsize (--pointsize)         :" ${POINTSIZE}
echo "  page size in lines              :" ${SPLITLINES}
echo "  max page count (-m, --max-pages):" $MAXPAGES
file=${POSITIONAL[0]}
dirname=$(dirname $(realpath $file))  # ensure we have absolute path name
file=$(basename $file)
basename=$([[ "$file" = *.* ]] && echo "${file%.*}" || echo "${file}")
if [ -z "$basename" ]; then
    echo "please specify the input file"
    exit 1
fi
echo "  input file: " $dirname/$file
echo "splitting $file into chunks of $SPLITLINES lines"
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

## Split, eventually decompress
echo $(file -b -i $dirname/$file)
if [ "$(file -b -i $dirname/$file)" == "application/x-bzip2; charset=binary" ]; then
    # bz2 compressed
    echo "bz2 compressed file"
    bzip2 -dc  $dirname/$file | split --lines=${SPLITLINES} - "${basename}-chunk-" || exit 2
    echo "split"
else
    echo "uncompressed text"
    split -l $SPLITLINES $dirname/$file "${basename}-chunk-" || exit 2
fi

## rename chunks back to .txt so it is easier to handle this afterwards
for subfile in ${basename}-chunk-* ; do
    mv $subfile $subfile.txt
done

## main conversion loop
n=$(ls ${basename}-chunk-*.txt|wc -l)
i=1  # counts pages
for subfile in ${basename}-chunk-*.txt ; do
    echo " -- "$subfile "($i/$n)"
    # Extract just the name of the file without extention
    subbase=${subfile%.txt}

    ## Convert text to jpg
    ## Play with font and point size
    ## Uses "annotate", intended for adding text to images
    convert -size 3000x2000 xc:white -pointsize $POINTSIZE\
	    -fill black\
	    -font $FONT\
	    -annotate +$POINTSIZE+$POINTSIZE "@$subfile"\
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
    if [ $i -gt $MAXPAGES ]; then
	# only process this many pages
	## find chunks that are not converted
	originalchunks=$(find . -regex ./${basename}-chunk-[^-]+.txt)
	convertedchunks=$(find . -regex ./${basename}-chunk-.+-converted.txt | sed -e 's/-converted//g')
	echo "all $MAXPAGES pages done"
	unconverted=$(grep -x -v -F -f <(echo "$convertedchunks") <(echo "$originalchunks"))
	rm $unconverted
	echo "done"
	break
    fi
done
echo "All done :-)"
