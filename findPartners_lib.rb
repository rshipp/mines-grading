require 'shellwords'

class Name
    attr_accessor :first_name, :last_name, :username
    def initialize(first_name, last_name)
        @first_name = first_name
        @last_name = last_name
        @needFirst = false
    end
    # in the format last,\s*first
    def initialize(fullName)
        @first_name = fullName.split(/\W+/)[0]
        @last_name = fullName.split(/\W+/)[1]
        @needFirst = false
    end

    def setNeedFirst
        @needFirst = true
        puts "INFO: Found duplicate last name"
    end

    def getRegex
        Regexp.new("#{@first_name[0..2]}.*#{@last_name}")
    end

end

def isText?( file_path )
    type = `file -b --mime-type #{Shellwords.escape(file_path)}`
    if type[0..4] == "text/"
        true
    else
        false
    end
end

def findFiles( username, prestring )
    # returns a list of files associated with a given user
    Dir.glob(File.join("#{username}*", "**" )) + Dir.glob("#{prestring}_#{username}_*") + ["#{username}.txt"] 
end

def searchFiles( regex, files )
    # returns files of the files given that match the regex
    # does not search binary/application files (only text)
    file_matches = Array.new
    files.each do |file_path|
        next if !isText?(file_path)
        file = File.new(file_path)
        file.each do |line|
            begin
                if regex.match( line )
                    file_matches << file_path
                    break
                end
            rescue Exception => msg
                #$stderr.puts "Bad file #{file_path} skipped"
            end
        end
    end
    file_matches
end
