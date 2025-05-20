#!/usr/bin/env python3
import sys
from lxml import etree

def group_paths(infile, outfile):
    # parse SVG
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(infile, parser)
    root = tree.getroot()

    # gather all <path> elements
    paths = root.findall('.//{http://www.w3.org/2000/svg}path')

    # a trivial “group by fill hue” placeholder:
    # here we just alternate into 10 buckets
    buckets = {i: [] for i in range(10)}
    for i, p in enumerate(paths):
        # get the fill color (e.g. "#4F05C2")
        fill = p.get('fill', '')
        # hash to bucket 0–9
        b = hash(fill) % 10
        buckets[b].append(p)

    # remove all original paths
    for p in paths:
        parent = p.getparent()
        parent.remove(p)

    # create <g> for each bucket, re-insert
    for b in range(10):
        g = etree.SubElement(root, 'g', id=f'group{b}')
        for p in buckets[b]:
            g.append(p)

    # write out prettified SVG
    tree.write(outfile, pretty_print=True, xml_declaration=True, encoding='utf-8')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 group_svg_paths.py input.svg output.svg")
        sys.exit(1)
    group_paths(sys.argv[1], sys.argv[2])
