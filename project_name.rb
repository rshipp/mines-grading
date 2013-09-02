#! /usr/bin/env ruby
#
# Copyright © 2013 Andrew DeMaria (muff1nman) <ademaria@mines.edu>
#
# All Rights Reserved.

# A simple script to get the project name given that the entire portfolio of
# student submissions have been downloaded through black board and is in the
# format of: 
#
#   gradebook_(spring|fall)<YEAR>-<DEPARTMENT><COURSE_NUM><SECTION>_<PROJECTNAME>.zip
#

def find_dir_like( options={} )
  Dir.glob("*.zip").each do |file|
    if file =~ /gradebook_(?:spring|fall)\d{4}-CSCI\d{3}._(.*)\.zip/
      if options[:project_name_only]
        return $1
      else
        return file
    end
  end
end

puts find_dir_like

