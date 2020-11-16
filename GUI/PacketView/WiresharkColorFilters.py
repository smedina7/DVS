import os

class WiresharkColors():
    def __init__(self, dataline, color):
        rgb_val = str(color)
        keyword = dataline
        tty_standard_color = self.scaleRGB(rgb_val)

        self.setFilterRule(keyword, tty_standard_color) 
    
    def scaleRGB(self, rgb_val):
        rgb = rgb_val.strip("()")
        color = rgb.split(",")
        scale = .00398

        r = int(color[0])/scale
        red = int(r)

        g = int(color[1])/scale
        green = int(g)

        b = int(color[2])/scale
        blue = int(b)

        return "["+str(red)+", "+str(green)+", "+str(blue)+"]"

    def setFilterRule(self, keyword, tty_standard_color):
        custom_filter = keyword.lower()
        blacktext = "[0,0,0]"
        colortext = ""
        #newRule = "@"+keyword+"@"+custom_filter+"@"+tty_standard_color+blacktext
        if keyword == "Keypresses":
            newRule = "@"+"Keypress Log"+"@"+"keypresses"+"@"+tty_standard_color+blacktext
            colortext = tty_standard_color
        if keyword == "Timed Screenshots":
            newRule = "@"+"TimedScreenshots Log"+"@"+"timedscreenshots"+"@"+tty_standard_color+blacktext
        if keyword == "System Calls":
            newRule = "@"+"New coloring rule"+"@"+"systemcalls and keypresses@"+tty_standard_color+blacktext
        if keyword == "Mouse Clicks":
            newRule = "@"+"MouseClicks Log"+"@"+"mouseclicks"+"@"+tty_standard_color+blacktext

        self.appendToColorFilterFile(newRule+"\n")
        
    def appendToColorFilterFile(self, newRule):
        path = os.path.abspath("GUI/PacketView/colorFilters.txt")

        if "New coloring rule" in newRule:
            _file = open(path, 'r+')
            existingRules = _file.read()
            _file.seek(0,0)
            _file.write(newRule)
            _file.write(existingRules)
        else:
            _file = open(path, 'a+')
            _file.write(newRule)

        _file.close()

def clearFilters():
    path = os.path.abspath("GUI/PacketView/colorFilters.txt")
    _file = open(path, 'w').close()