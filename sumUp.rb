#!/usr/bin/env ruby

require 'tempfile'

def badUsage
    puts "Usage: ./sumUp.rb filename"
    exit(1)
end

def badFile
    puts "Could not deal with that shitty file"
    exit(1)
end

def checkArgs
    badUsage unless ARGV.length == 1
    badFile unless File.readable?( ARGV[0]) and File.writable?( ARGV[0] )
end

checkArgs

pointsLine = /.*\s+(-?\d+\.?\d*|-?\d*\.\d+)$/
totalLine = /^Total\s*(-?\d+\.?\d*|-?\d*\.\d+)?$/
endLine = /.*=+.*/
points = 0
newFile =  {
    :before => "",
    :after => ""
}
spaces = 4
current = :before
File.open( ARGV[0], "r" ) do |file|
    file.each do |line|
        # switch to after
        if line =~ totalLine
            current = :after
            next
        end

        #save for later
        spaces = line.length if line =~ endLine

        newFile[current] += line
        points += $1.to_f if pointsLine =~ line and current != :after
    end
end

# test for a nice round number and if so do int
points = points.to_i if points.to_i == points
# make sure points is positive
points = 0 unless points > 0
# calc the correct number of spaces for total display
spaces -= "Total".length + points.to_s.length + 1

File.open( ARGV[0], "w" ) do |file|
    file.write(newFile[:before])
    file.write( "Total#{" " * spaces}#{points}\n")
    file.write(newFile[:after])
end
