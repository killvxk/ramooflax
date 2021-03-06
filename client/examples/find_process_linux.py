#!/usr/bin/env python
#
# We are looking for "argv[1]" running under debian
#
# We install the Linux26.find_process_filter on cr3 writes
# The framework will call our filter Before each write
#
from ramooflax import VM, CPUFamily, Utils, OSAffinity
import sys

if len(sys.argv) < 2:
    print "gimme prog name"
    sys.exit(-1)

# Target process
process_name = sys.argv[1]

# Some offsets for debian 2.6.32-5-486 kernel
settings = {"thread_size":8192, "comm":540, "next":240, "mm":268, "pgd":36}
os = Utils.create_os(OSAffinity.Linux26, settings)
hook = os.find_process_filter(process_name)

#
# Main
#
vm = VM(CPUFamily.AMD, "192.168.254.254:1234")

vm.attach()
vm.stop()
vm.cpu.filter_write_cr(3, hook)

while not vm.resume():
    continue

vm.cpu.release_write_cr(3)
print "success: %#x" % (os.get_process_cr3())
vm.detach()
