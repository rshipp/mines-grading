#!/usr/bin/env ruby

require 'shellwords'

# Translates a given full name (last and first) to a username.  Requires a list
# of usernames

def searchFor (partial_first, partial_last)
    searh_for = "#{partial_first.downcase}.*#{partial_last.downcase}.*"
    #puts "Searching for: #{searh_for}"
    `grep -P "#{searh_for}" #{Shellwords.escape(ARGV[0])}`.split(/\W+/)
end


usage = "./script <usernames> first_name last_name"

abort(usage) if ARGV.length != 3

first_name = ARGV[1]
last_name = ARGV[2]

# algorithm:
#   start search with:
#     first letter of first name --- anything --- first three letters of last
#     name  --- anything
#
#   and then narrow down the search by including letters from the last name and
#   user name till there is only one result.  If there are no results, return
#   cannot translate

partial_last = ""
partial_first = ""
usernames = []

    # note the unless prevents the partial_XXXX from repeating
last_name.each_char do |last_name_char|
    partial_last += last_name_char
    usernames = searchFor( partial_first, partial_last )
    break if usernames.length <= 1 and !(partial_last.length <= 2) # force use of first two characters
end

#usernames.each { |user| puts "Match: #{user}"}

# step back, becuase we will now try to distinguish based on first name
partial_last = partial_last[0...-1] if usernames.length == 0 and partial_last.length > 0
usernames = searchFor( partial_first, partial_last )

first_name.each_char do |first_name_char|
    break if usernames.length <= 1 and !(partial_first.length < 1) # force use of first character
    partial_first +=  first_name_char
    usernames = searchFor( partial_first, partial_last )
end

case usernames.length
    when 1 then puts usernames[0]
    when 0 then abort("Could not find a suitable match")
    else abort("More than one: #{usernames.join(',')}")
end

