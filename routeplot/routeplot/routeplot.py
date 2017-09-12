#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 12:02:51 2017

@author: Vijayasai S
"""


class GoogleRoutePlotter():

    def __init__(self,data,doc="my_map.html",title="Anil",zoom=13,height=500):
        self.data = data
        self.zoom = zoom
        self.height = height
        self.doc = open(doc,"w")
        self.title =title

    def centroid(self):
        lat = []
        lng = []
        for value in self.data:
            lat.append(value[0])
            lng.append(value[1])
        return sum(lat)/len(lat),sum(lng)/len(lng)

    def header_lines(self):
        # Header lines for html
        self.doc.write("<!DOCTYPE html>\n")
        self.doc.write("<html>\n")
        self.doc.write("<head>\n")
        self.doc.write("<title> "+self.title+" </title>\n")
        return

    def css_lines(self):
        # CSS script lines
        self.doc.write("<style type=\"text/css\"> #map-canvas { height: "+str(self.height)+"px }; </style>\n")
        self.doc.write("<script type=\"text/javascript\" src=\"https://maps.googleapis.com/maps/api/js?v=3.22\"></script>\n")
        self.doc.write("<script type=\"text/javascript\">\n\n")
        return

    def js_lines(self):
        # init function
        self.doc.write("function init() {\n")
        self.doc.write("\tvar mapOptions = {\n")
        lat,lng = self.centroid()
        self.doc.write("\t\tcenter: new google.maps.LatLng("+str(lat)+","+str(lng)+"),\n")
        self.doc.write("\t\tzoom: "+str(self.zoom)+",\n")
        self.doc.write("\t};\n")
        self.doc.write("\tmap = new google.maps.Map(document.getElementById(\'map-canvas\'), mapOptions);\n")
        self.doc.write("\tinfo = document.getElementById(\'info\');\n")
        self.doc.write("\tpointsToPath();\n")
        self.doc.write("}\n\n")
        # Points To Path function
        self.doc.write("var path = [];\n")
        self.doc.write("function pointsToPath () {\n")
        self.doc.write("\tvar sArray = [\n")

        for value in self.data:
            self.doc.write("\t\""+str(value[0])+","+str(value[1])+"\",\n")

        self.doc.write("\t];\n\n")
        self.doc.write("\tfor (var i=0; i < sArray.length; i++) {\n")
        self.doc.write("\t\ts = sArray[i].split(\",\");\n")
        self.doc.write("\t\tpoint = new google.maps.LatLng(s[0],s[1]);\n")
        self.doc.write("\t\tpath.push(point);\n")
        self.doc.write("\t}\n")
        self.doc.write("\tbatchJobs();\n")
        self.doc.write("}\n\n")
        # Batch jobs function
        self.doc.write("var batch = [];\n")
        self.doc.write("var items = 8;\n")
        self.doc.write("function batchJobs() {\n\n")
        self.doc.write("\tfor (var i=0; i < path.length; i++) {\n")
        self.doc.write("\t\tbatch.push(path[i]);\n")
        self.doc.write("\t\tif (i == items || i == path.length - 1 ) {\n")
        self.doc.write("\t\t\tcalcRoute();\n")
        self.doc.write("\t\t\tbatch = [path[i]];\n")
        self.doc.write("\t\t\titems += items\n")
        self.doc.write("\t\t}\n")
        self.doc.write("\t}\n")
        self.doc.write("}\n\n")
        # Calculating the route
        self.doc.write("function calcRoute() {\n\n")
        self.doc.write("\trStart = batch[0];\n")
        self.doc.write("\trEnd = batch[batch.length -1];\n\n")
        self.doc.write("\twaypoints = [];\n\n")
        self.doc.write("\tfor (var i = 1; i< batch.length -2; i++) {\n")
        self.doc.write("\t\twaypoints.push({\n")
        self.doc.write("\t\tlocation: batch[i],\n")
        self.doc.write("\t\tstopover: true\n")
        self.doc.write("\t\t });\n")
        self.doc.write("\t}\n")
        self.doc.write("\tvar request = {\n")
        self.doc.write("\t\torigin: rStart,\n")
        self.doc.write("\t\tdestination: rEnd,\n")
        self.doc.write("\t\twaypoints: waypoints,\n")
        self.doc.write("\t\ttravelMode: google.maps.TravelMode.DRIVING\n")
        self.doc.write("\t};\n")
        # only 23 way points are allowed
        self.doc.write("\tdirectionsService = new google.maps.DirectionsService;\n")
        self.doc.write("\tpoly = new google.maps.Polyline({map: map});\n")
        self.doc.write("\tline =[];\n\n")
        self.doc.write("\tdirectionsService.route(request, function(result, status) {\n")
        self.doc.write("\t\tif (status == google.maps.DirectionsStatus.OK) {\n")
        self.doc.write("\t\t\tfor(var i = 0, len = result.routes[0].overview_path.length; i < len; i++) {\n")
        self.doc.write("\t\t\t\tline.push(result.routes[0].overview_path[i]);\n")
        self.doc.write("\t\t\t\t}\n")
        self.doc.write("\t\t\tpoly.setPath(line);\n")
        self.doc.write("\t\t} else {\n")
        self.doc.write("\t\t\talert(\'Directions request failed due to\' + status);\n")
        self.doc.write("\t\t}\n")
        self.doc.write("\t});\n")
        self.doc.write("}\n")
        self.doc.write("google.maps.event.addDomListener(window, 'load', init);\n")
        return

    def footer_lines(self):
        self.doc.write("</script>\n")
        self.doc.write("</head>\n")
        self.doc.write("\t<body>\n")
        self.doc.write("\t\t<div id=\"map-canvas\"></div>\n")
        self.doc.write("\t\t<div id=\"info\" >0 / 0</div>\n")
        self.doc.write("\t</body>\n")
        self.doc.write("</html>\n")

    def draw(self):
        self.header_lines()
        self.css_lines()
        self.js_lines()
        self.footer_lines()

        return

# if __name__ == "__main__":
#data = [[18.6231941151,73.7158857139], [18.6193690456,73.7111026582], [18.5939944423,73.7354528121],
#                          [18.594067781,	73.7355691226], [18.5911107433,	73.7412058862], [18.5909474502,	73.7520726129],
#                         [18.5911525692,	73.7578107901], [18.5747092396,	73.7638577918], [18.5747327309,	73.7638343005], [18.4871927272,	73.7961709198],
#                         [18.4876310403,	73.7955693136], [18.4876573964,	73.795632912], [18.4803178009,	73.8047544078],
#                        [18.4629909695,	73.8201010953], [18.4629909695,	73.8201010953], [18.3554025828,	73.853297725],
#                        [18.313239156,	73.8656426841], [18.3135073004,	73.8658861914], [18.2105272171,	73.9327779246],
#                         [18.0232454903,	74.0245629761], [18.0166140712,	74.0212942491], [17.9973191282,	73.9943061953],
#                         [17.9973953317,	73.9943594804], [17.9658505406,	73.9852975722], [17.9398290674,	73.895239417],
#                         [17.9477003683,	73.8878224721], [17.947813814,	73.8876958483], [17.9420487078,	73.8705558014],
#                        [17.9407074125,	73.8648961195], [17.9320872552,	73.8505945079], [17.9296006162,	73.8346874672],
#                         [17.9417221216,	73.8307042612], [17.9461906232,	73.8333243994], [17.9320574613,	73.8132725785],
#                        [17.9219172457,	73.7947757664], [17.9233937592,	73.7797126933], [17.9228574703,	73.7392824652],
#                         [17.9232373416,	73.7354808871], [17.917615475,	73.7183775095], [17.9343023119,	73.6701160877], [17.9342839772,	73.6701109311],
#                            [17.9342507456,	73.6700874398], [17.9343504404,	73.6701728106], [17.9262373512,	73.6657008712], [17.9054389656,	73.6630910463],
#                         [17.9054189121,	73.6634141947], [17.8715152518,	73.6742241986], [17.8005102512,	73.7069011551],
#                        [17.7970421347,	73.7102008219], [17.7911635828,	73.7169256332], [17.7824488873,	73.7246760398],
#                     [17.7769502067,	73.7218828682], [17.7991105141,	73.6925359452]]
#
#gmap = GoogleRoutePlotter(data,doc="Anil.html")
#gmap.draw()