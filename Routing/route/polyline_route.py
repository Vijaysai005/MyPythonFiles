#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 17:42:40 2017

@author: vijayasai
"""

class PolylineRoute(object):


    def __init__(self):
        pass


    def decode_polyline(self, point_str):
        """
        Decodes a polyline that has been encoded using Google's algorithm
        http://code.google.com/apis/maps/documentation/polylinealgorithm.html

        This is a generic method that returns a list of (latitude, longitude)
        tuples.

        :param point_str: Encoded polyline string.
        :type point_str: string
        :returns: List of 2-tuples where each tuple is (latitude, longitude)
        :rtype: list
        """

        # some coordinate offset is represented by 4 to 5 binary chunks
        coord_chunks = [[]]
        for char in point_str:

            # convert each character to decimal from ascii
            value = ord(char) - 63

            # values that have a chunk following have an extra 1 on the left
            split_after = not (value & 0x20)
            value &= 0x1F

            coord_chunks[-1].append(value)

            if split_after:
                    coord_chunks.append([])

        del coord_chunks[-1]

        coords = []

        for coord_chunk in coord_chunks:
            coord = 0

            for i, chunk in enumerate(coord_chunk):
                coord |= chunk << (i * 5)

            # there is a 1 on the right if the coord is negative
            if coord & 0x1:
                coord = ~coord  # invert
            coord >>= 1
            coord /= 100000.0

            coords.append(coord)

        # convert the 1 dimensional list to a 2 dimensional list and offsets to
        # actual values
        points = []
        prev_x = 0
        prev_y = 0
        for i in range(0, len(coords) - 1, 2):
            if coords[i] == 0 and coords[i + 1] == 0:
                continue

            prev_x += coords[i + 1]
            prev_y += coords[i]
            # a round to 6 digits ensures that the floats are the same as when
            # they were encoded
            points.append([round(prev_x, 6), round(prev_y, 6)])

        return points


    def polyline_route(self, direction_legs):

        polylines = []
        for leg in direction_legs:
            for step in leg["steps"]:
                polylines.append(step['polyline']['points'])

        locations = [self.decode_polyline(x) for x in polylines]
        locations = [x for y in locations for x in y]

        lat = [x[1] for x in locations]
        lng = [x[0] for x in locations]
        return lat, lng


if __name__ == "__main__":

    PR = PolylineRoute()
    out = PR.polyline_route(route)