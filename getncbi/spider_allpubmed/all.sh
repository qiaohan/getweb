#!/bin/bash
for((i=0;i<100;i++));
do
	python allpubmed.py $[i*500] $[i*500+500]
done
