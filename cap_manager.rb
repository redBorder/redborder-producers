#!/usr/bin/env ruby
require 'optparse'

def usage
  puts "Usage: #{$0} [options]"
  puts "Options: -p: directory of pcaps"
  puts "         -c: path to pmacct config file"
  puts "running this script will manage differences between caps or pcaps and make safe rewrites over the original ips"
  puts "then it will start replaying the pcaps, hoping somebody is listening, like a flow sensor."
end
def parse_args
  options = {}
  parser = OptionParser.new do |opts|
    opts.banner = usage
    opts.on('-p', '--path PATH', 'Path to pcap directory') { |path| options[:path] = path }
    opts.on('-c', '--config CONFIG', 'Path to pmacct config file') { |config| options[:config] = config }
  end

  parser.parse!
  options[:path] ||= '/home/ljblanco/Descargas/w3stomz/'
  options[:config] ||= '/home/ljblanco/Repos/redborder/ng/pmacct/pmmactd_synth.conf'
  options
end

def list_files(path)
  Dir.glob(File.join(path, '**', '*')).select { |f| File.file?(f) }
end

def open_pmacct(args)
  container = 'pmacct/pmacctd:latest'
  container_running = system("docker ps | grep #{container}")
  return if container_running

  puts 'Starting pmacct docker container...'
  system("sudo docker run --privileged --network host -v #{args[:config]}:/etc/pmacct/pmacctd.conf #{container}")
end

def get_pcap_files(args)
  unless Dir.exist?(args[:path])
    puts "Error: Directory #{args[:path]} does not exist"
    exit 1
  end

  files = list_files(File.absolute_path(pcap_dir))
  if files.empty?
    puts "No files found in #{pcap_dir}"
    exit 1
  end
  files
end

def put_interface_up()
  interface_exists = system("ip link show eth1 > /dev/null 2>&1")
  unless interface_exists
    puts "Creating dummy interface eth1..."
    system("sudo modprobe dummy")
    system("sudo ip link add eth1 type dummy")
    system("sudo ifconfig eth1 hw ether 00:11:22:33:44:55")
  end

  is_ip_configured = system("ip addr show eth1 | grep '10.1.32.201' > /dev/null 2>&1")
  unless is_ip_configured
    puts "Configuring IP address for eth1..."
    system("sudo ip addr add 10.1.32.201/24 dev eth1 label eth1:0")
  end

  is_interface_up = system("ip link show eth1 | grep 'UP' > /dev/null 2>&1")
  unless is_interface_up
    puts "Bringing up interface eth1..."
    system("sudo ip link set eth1 up")
  end

  is_promisc = system("ip link show eth1 | grep 'PROMISC' > /dev/null 2>&1")
  unless is_promisc
    puts "Setting eth1 to promiscuous mode..."
    system("sudo ip link set eth1 promisc on")
  end
end

def main
  args = parse_args

  put_interface_up
  caps = get_pcap_files(args)
  open_pmacct(args)
  caps.each do |file|
    begin
      # Process each file
      puts "Processing: #{file}"
      pcap_file = "#{File.dirname(file)}/#{File.basename(file, '.cap')}.pcap"
      system("editcap -F pcap #{file} #{pcap_file}") unless File.exist?(pcap_file)
      rewritten_file = "#{File.dirname(file)}/#{File.basename(file, '.pcap')}_rewritten.pcap"
      system("tcprewrite --infile=#{pcap_file} --outfile=#{rewritten_file} --pnat=10.0.0.0/8:11.0.0.0/8") unless File.exist?(rewritten_file)
    rescue StandardError => e
      puts "Error processing #{file}: #{e.message}"
    end
  end
end

if $PROGRAM_NAME == __FILE__
  main
end
