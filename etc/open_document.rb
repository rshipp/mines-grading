#! /usr/bin/env ruby
#
# Copyright © 2013 Andrew DeMaria (muff1nman) <ademaria@mines.edu>
#
# All Rights Reserved.

# Opens either a docx or a pdf file from the command line

require 'shellwords'

type_to_program = {
  'text/plain' => 'gvim',
  'application/pdf' => 'okular',
  'application/msword' => 'libreoffice'
}


given_file = `file --mime-type --brief #{Shellwords.escape ARGV[0]}`.chomp
puts "File type is [#{given_file}]"

if type_to_program[ given_file ]
  running = fork do
    `#{type_to_program[ given_file ]} #{Shellwords.escape ARGV[0]}`
  end
  Process.detach running
else
  puts "Not a valid file type"
end
  

