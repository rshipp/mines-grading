#!/usr/bin/env ruby


# check args
abort("Usage: ./script prestring directory") unless ARGV.length == 2 or ARGV.length == 1
$pre_string = ARGV[0]
$directory = ARGV[1]
$directory ||= Dir.getwd
$student_submission = /^#{Regexp.quote($pre_string)}_([^_]*)_attempt_(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})(_[^\.]*)?\..*$/ 

def isSubmission?( string )
    !($student_submission =~ string).nil?
end

def getUsername( string )
    string.split("_")[1]
end

Dir[File.join($directory, "*.txt")].each do |file|
    puts getUsername( File.basename( file )) if  isSubmission?( File.basename( file ))
end

