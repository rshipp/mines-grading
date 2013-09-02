#!/usr/bin/env bash
find . -maxdepth 1 -ilname "*" -printf "%f -> %l\n" | sort
