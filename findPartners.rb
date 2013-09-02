#!/usr/bin/env ruby

require 'shellwords'
require_relative 'findPartners_lib.rb'

usage = "script <fullListofNames> <fullListofUserNames> prestring"

abort( usage) unless ARGV.length == 3
pre_string = ARGV[2]

partners = Hash.new()

users_with_submissions = `findUsernames.rb #{Shellwords.escape(pre_string)}`.split(/\W+/)

all_names = []
# populate user_names with all the user, first and last names
File.read(ARGV[0]).split(/[^\w,]+/).collect { |text| all_names <<  Name.new(text) }

# Place additional seach restraints on users that have the same last name
# Also populate their usernames
all_names.each do |name|
    name.setNeedFirst if all_names.count{|other_name| other_name.last_name == name.last_name } > 1
    name.username = `translateNameToUsername.rb #{Shellwords.escape(ARGV[1])} #{name.first_name} #{name.last_name}`.chomp
end

users_with_submissions.each do |current_username|
    users_files = findFiles( current_username, pre_string )
    all_names.each do |other_name|
        # skip looking for the user when we are in his files
        next if other_name.username == current_username
        files_matching = searchFiles( other_name.getRegex, users_files )
        if files_matching.size > 0 and partners[other_name.username] != current_username
            if !(partners[other_name.username].nil?)
                $stderr.puts "Oh shit! whats going on here!"
            else
                puts "#{other_name.username} is referenced in #{current_username}'s submission"
                partners[other_name.username] = current_username
            end
        end
    end
end
    
$stderr.print "Would you like to create sym links for partners? [y/n]: "
input = $stdin.gets.chomp

if (input == "Y" or input == "y")
    $stderr.puts "Creating sym links"
    partners.each do |found, link_to|
        puts "ln -s #{link_to}.txt #{found}.txt"
        `ln -s #{link_to}.txt #{found}.txt`
        if $?.to_i != 0
            $stderr.print "  Would you like to force this sym link? [WARNING: OVERWRITE] [y/n]: "
            overwrite = $stdin.gets.chomp
            if (overwrite == "Y" or overwrite == "y")
                puts "  ln -fs #{link_to}.txt #{found}.txt"
                `ln -fs #{link_to}.txt #{found}.txt`
            end
            puts ""
        end
    end
    $stderr.puts "Done"
end
    

