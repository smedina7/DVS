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
    if pinfo.abs_ts >= 1602705117.0 and pinfo.abs_ts <= 1602705119.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602705117.5220861_xfdesktop_root.png")

       subtree:add(timestamp_F,tostring("2020-10-14T19:51:57"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602705145.0 and pinfo.abs_ts <= 1602705147.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602705145.4567268_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-14T19:52:25"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602705144.0 and pinfo.abs_ts <= 1602705146.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602705144.0892322_qterminal_root.png")

       subtree:add(timestamp_F,tostring("2020-10-14T19:52:24"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602705111.0 and pinfo.abs_ts <= 1602705113.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602705111.8004274_xfdesktop_root.png")

       subtree:add(timestamp_F,tostring("2020-10-14T19:51:51"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602705108.0 and pinfo.abs_ts <= 1602705110.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602705108.14194_xfdesktop_root.png")

       subtree:add(timestamp_F,tostring("2020-10-14T19:51:48"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602705110.0 and pinfo.abs_ts <= 1602705112.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602705110.7452834_xfdesktop_root.png")

       subtree:add(timestamp_F,tostring("2020-10-14T19:51:50"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602705113.0 and pinfo.abs_ts <= 1602705115.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602705113.2492664_xfdesktop_root.png")

       subtree:add(timestamp_F,tostring("2020-10-14T19:51:53"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602705110.0 and pinfo.abs_ts <= 1602705112.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602705110.3347957_xfdesktop_root.png")

       subtree:add(timestamp_F,tostring("2020-10-14T19:51:50"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602705109.0 and pinfo.abs_ts <= 1602705111.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602705109.9720008_xfdesktop_root.png")

       subtree:add(timestamp_F,tostring("2020-10-14T19:51:49"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602705120.0 and pinfo.abs_ts <= 1602705122.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602705120.8296409_main.py_root.png")

       subtree:add(timestamp_F,tostring("2020-10-14T19:52:00"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602705118.0 and pinfo.abs_ts <= 1602705120.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602705118.2172499_xfdesktop_root.png")

       subtree:add(timestamp_F,tostring("2020-10-14T19:51:58"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602705108.0 and pinfo.abs_ts <= 1602705110.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602705108.7945545_xfdesktop_root.png")

       subtree:add(timestamp_F,tostring("2020-10-14T19:51:48"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602705109.0 and pinfo.abs_ts <= 1602705111.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602705109.5870864_xfdesktop_root.png")

       subtree:add(timestamp_F,tostring("2020-10-14T19:51:49"))
       subtree:add(eventdata_F, mycomplientstr)
    end
    if pinfo.abs_ts >= 1602705119.0 and pinfo.abs_ts <= 1602705121.0 then
       local subtree = tree:add(MouseClicks_proto,"MouseClicks Log")
       local mycomplientstr = tostring("/home/kali/eceld-netsys/eceld/plugins/collectors/pykeylogger/raw/click_images/1602705119.6514578_qterminal_root.png")

       subtree:add(timestamp_F,tostring("2020-10-14T19:51:59"))
       subtree:add(eventdata_F, mycomplientstr)
    end
end
-- register our protocol as a postdissector
register_postdissector(MouseClicks_proto)