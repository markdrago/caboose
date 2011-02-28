#!/bin/bash

#set default parameters
directory='.'
group='monthly'
metric='lines'
outfile='code-changes.out'
start_rev='0'

#get options from the command line
while getopts "d:g:o:m:s:" argparsed; do
    if [ "$argparsed" == "d" ]; then
        directory=$OPTARG
    elif [ "$argparsed" == "g" ]; then
        group=$OPTARG
    elif [ "$argparsed" == "o" ]; then
        outfile=$OPTARG
    elif [ "$argparsed" == "m" ]; then
        metric=$OPTARG
    elif [ "$argparsed" == "s" ]; then
        start_rev=$OPTARG
    fi
done

#absolute-ify the outfile path
if [ "${outfile:0:1}" != "/" ]; then
    wd=`pwd`
    outfile="${wd}/${outfile}"
fi

#empty output file
echo -n > $outfile

#setup grouping
group_seconds=$((60*60*24*30))

pushd $directory &> /dev/null

#get date of oldest commit in repo and today's date
moment=`hg log -r $start_rev --template "{date}" | cut -f1 -d.`
now=`date +%s`

#loop over revisions, jumping by group_seconds each time
while [ $moment -le $now ]; do
    #update to the revision just before the specified date
    hg up -d "<$moment 0"

    if [ "$metric" = "lines" ]; then
        result=`find . -type f -name '*.java' -print0 | wc -l --files0-from=- | tail -n 1 | awk '{print $1}'`
    elif [ "$metric" = "ncss" ]; then
        result=`javancss -recursive src/com | sed -e 's/.*: //'`
    elif [ "$metric" = "avgccn" ]; then
        result=`javancss -recursive -function src/com | grep 'Average Function CCN' | sed -e 's/.*: *//'`
    fi
    
    #produce output in outfile
    pretty_date=`date +%Y-%m --date=@$moment`
    echo "${pretty_date},${result}" >> $outfile
    
    #prepare for next loop iteration by adding group_seconds
    moment=$(($moment+$group_seconds))
done

popd &> /dev/null

