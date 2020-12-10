******************************************************
Move the following files from DVS/Wireshark_mod_files:
******************************************************
------------------------------------------------------
packet_list.cpp 
coloring_rules_dialog.cpp 
coloring_rules_dialog.h 
main_window_slots.cpp 
main_window.ui 
proto_tree.cpp 
proto_tree.h 
To -> /eceld-wireshark/wireshark-3.2.0/ui/qt/
------------------------------------------------------
CMakeOptions.txt 
To -> /eceld-wireshark/wireshark-3.2.0/
------------------------------------------------------
Go to this directory -> /eceld-wireshark/wireshark-3.2.0/build/
> sudo cmake ../
> sudo make install
This should install successfully! Go on to use the DVS system.
