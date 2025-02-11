#!/usr/bin/env ruby
# frozen_string_literal: true

require 'getopt/std'

def helper
  puts "Usage: rb_producer_simulator.rb [-h] [-s screen_name] [-a action]"
  puts "Options:"
  puts "  -a: Action to perform (start, restart, stop)"
  puts "  -s: Screen name (traffic, mitre_wide_attack, monitor, vault, scanner)"
  puts "  -h: Show this help message"
  exit 0
end

opt = Getopt::Std.getopts('a:s:h')

if opt['h']
  helper
  exit 0
end

VALID_SCREEN_NAMES = %w[traffic mitre_wide_attack monitor vault scanner 
bit_torrent] #custom incidents
screen_name ||= opt['s']
if !screen_name.nil? && !VALID_SCREEN_NAMES.include?(screen_name)
  puts "Error: Screen name must be one of: #{VALID_SCREEN_NAMES.join(', ')}"
  helper
  exit 1
end
screen_names = screen_name.nil? ? VALID_SCREEN_NAMES : [screen_name]

VALID_ACTIONS = %w[start restart stop] #start and restart do the same
action ||= opt['a']
unless !action.nil? && VALID_ACTIONS.include?(action)
  puts "Error: First argument must be 'start', 'restart' or 'stop'"
  helper
  exit 1
end

screen_names.each do |s|
  puts "Restarting screen instance #{s}"
  system("screen -X -S #{s} quit 2>/dev/null || true") # Kill screen instance if exists
  unless action == 'stop'
    if s == 'bit_torrent'
      system("screen -dmS #{s} ruby /usr/lib/redborder/bin/bit_torrent_producer.rb")
    else
      system("screen -dmS #{s} python3 /usr/lib/redborder/producers/py/#{s}.py")
    end
    puts "Screen instance #{s} created. Watch it running screen -r #{s}"
  end
end

system('screen -ls')
