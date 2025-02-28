#progressbar.printBar(len(absolute_file_list), len(absolute_file_list), prefix = 'Progress:', suffix = 'Complete', length = 50)


# Showing a progress bar for your operation

# for line in found_files:
#    print(line)




#  ====================== Div Test code  ======================
#scrapbook = scrapbook.ScrapBook
#scrapbook.simpleCalc()
#scrapbook.endless_loop()

context = Context()

#devices = Devices.from_device_file(context, '/dev/sda')

#for partition in device.device_node:
#    print(partition)

#print(pyudev.Devices.from_name(context, 'block', 'sda'))

device_list = []
partition_list = []

from treelib import Node, Tree
tree = Tree()
#tree.create_node("Harry", "harry")  # root node
#tree.create_node("Jane", "jane", parent="harry")
#tree.create_node("Bill", "bill", parent="harry")
#tree.create_node("Diane", "diane", parent="jane")
#tree.create_node("Mary", "mary", parent="diane")
#tree.create_node("Mark", "mark", parent="jane")
#tree.show()


for key, device in enumerate(context.list_devices()):
    pass


tree.create_node("Devices", "devices")  # root node
for device in context.list_devices(subsystem='block', DEVTYPE='partition'):
    tree.create_node(device.find_parent('block').device_node, device_list.append(device.parent.device_node), parent="devices")

tree.show()
    #print(device)
    #usbdevice = device.get('ID_USB_DRIVER')
    #device_list.append(device.parent.device_node.split('/')[2])
    #device_list.append(device.parent.device_node)

    #for partition in device.parent.children:
    #    partition_list.append(partition)

    #print(partition)
    #print('{0} is located on {1}'.format(device.device_node, device.find_parent('block').device_node))

    #a = []
    #b = []
    #a = [[device.find_parent('block').device_node], [b.append(device.device_node)]]


    #print(device.get('ID_FS_LABEL', 'unlabeled partition'))
    #print(partitions)
    #print ("{} - ({}): {} on {}".format(device.device_node, device.device_type, device.get('ID_FS_TYPE'), device.parent.device_node))
    #print (device)


#print(a)

#for device in device_list:
    #print (device)




    #for partition in pyudev.Devices.from_name(context, 'block', 'sda'):
        #print (partition.getDEVNAME)

    #if usbdevice == 'usb-storage':
        #print("{0} {1}".format(device.device_node, device.get('ID_FS_UUID')))
        #print(usbdevice)
# ======================================================================================================================


#  ====================== Showing GUI  ======================
#treeview = TreeViewFilterWindow(Gtk.Window, filepath_index)
# ==========================================================

#  ====================== Writing file index JSON file to logs directory  ======================
#filepath_index_list = list() # Converting a set() to a list() type

#filepath_index_json = json.decoder(filepath_index) # Dumps list to json syntax
#json_fh = open(backup_json_file, "w")
#json_fh.write(str(filepath_index_json))
#json_fh.close()
# ==============================================================================================

print("")