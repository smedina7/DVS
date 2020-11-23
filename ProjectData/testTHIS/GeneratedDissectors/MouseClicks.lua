-- MouseClicks frame number-based postdissector
-- declare Fields to be read
-- declare our (pseudo) protocol
MouseClicks_proto = Proto("mouseclicks","MouseClicks Log")
-- create the fields for our "protocol"
timestamp_F = ProtoField.string("mouseclicks.timestamp","Original Event Timestamp")
eventdata_F = ProtoField.string("mouseclicks.data","Log Data")

-- add the field to the protocol
MouseClicks_proto.fields = {timestamp_F, eventdata_F}

-- create a function to "postdissect" each frame
function MouseClicks_proto.dissector(buffer,pinfo,tree)
    -- add the data based on timestamps
    if pinfo.abs_ts >= 1602036149.0 and pinfo.abs_ts <= 1602036151.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036149.3312886_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:29"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036167.0 and pinfo.abs_ts <= 1602036169.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036167.28679_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:47"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036132.0 and pinfo.abs_ts <= 1602036134.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036132.6176386_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:12"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036136.0 and pinfo.abs_ts <= 1602036138.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036136.4715183_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:16"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036150.0 and pinfo.abs_ts <= 1602036152.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036150.0325723_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:30"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036149.0 and pinfo.abs_ts <= 1602036151.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036149.1436486_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:29"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036170.0 and pinfo.abs_ts <= 1602036172.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036170.0911806_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:50"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036142.0 and pinfo.abs_ts <= 1602036144.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036142.3974845_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:22"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036123.0 and pinfo.abs_ts <= 1602036125.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036123.1183212_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:03"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036157.0 and pinfo.abs_ts <= 1602036159.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036157.2843206_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:37"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036144.0 and pinfo.abs_ts <= 1602036146.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036144.3855362_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:24"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036133.0 and pinfo.abs_ts <= 1602036135.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036133.9036856_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:13"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036171.0 and pinfo.abs_ts <= 1602036173.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036171.375012_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:51"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036127.0 and pinfo.abs_ts <= 1602036129.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036127.563375_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:07"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036129.0 and pinfo.abs_ts <= 1602036131.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036129.7025251_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:09"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036131.0 and pinfo.abs_ts <= 1602036133.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036131.4408488_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:11"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036152.0 and pinfo.abs_ts <= 1602036154.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036152.8575513_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:32"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036122.0 and pinfo.abs_ts <= 1602036124.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036122.2287035_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:02"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036130.0 and pinfo.abs_ts <= 1602036132.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036130.5824332_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:10"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036134.0 and pinfo.abs_ts <= 1602036136.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036134.8055806_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:14"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036146.0 and pinfo.abs_ts <= 1602036148.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036146.5485303_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:26"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036158.0 and pinfo.abs_ts <= 1602036160.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036158.4855525_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:38"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036155.0 and pinfo.abs_ts <= 1602036157.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036155.1241307_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:35"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036152.0 and pinfo.abs_ts <= 1602036154.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036152.0071542_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:32"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036125.0 and pinfo.abs_ts <= 1602036127.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036125.6207025_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:05"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036148.0 and pinfo.abs_ts <= 1602036150.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036148.220126_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:28"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036148.0 and pinfo.abs_ts <= 1602036150.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036148.4042437_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:28"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036166.0 and pinfo.abs_ts <= 1602036168.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036166.60355_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:46"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036128.0 and pinfo.abs_ts <= 1602036130.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036128.6833673_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:08"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036160.0 and pinfo.abs_ts <= 1602036162.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036160.2586162_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:40"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036139.0 and pinfo.abs_ts <= 1602036141.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036139.0928006_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:19"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036149.0 and pinfo.abs_ts <= 1602036151.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036149.8292172_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:29"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602036162.0 and pinfo.abs_ts <= 1602036164.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602036162.8077326_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-07T02:02:42"))
       subtree:add(eventdata_F, mycomplientstr)
    end
end
-- register our protocol as a postdissector
register_postdissector(MouseClicks_proto)