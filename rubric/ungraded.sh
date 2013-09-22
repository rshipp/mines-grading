#!/bin/bash
grep -l "Total\s*$" *.txt | sed 's/\.txt//' | sed '/Rubric/d'

