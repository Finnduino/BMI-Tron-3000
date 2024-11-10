from lxml import etree

def remove_elements_from_svg(input_file, output_file):
    tree = etree.parse(input_file)
    root = tree.getroot()

    # Namespace dictionary to handle namespaces in the SVG
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}

    # Find and remove all <line> elements
    #for line in root.findall('.//svg:line', namespaces):
    #    parent = line.getparent()
    #    parent.remove(line)

    # Find and remove all <clipPath> elements
    #for clipPath in root.findall('.//svg:clipPath', namespaces):
    #    parent = clipPath.getparent()
    #    parent.remove(clipPath)
    
    for path in root.findall('.//svg:path', namespaces):
        parent = path.getparent()
        parent.remove(path)

    # Write the modified tree to the output file
    tree.write(output_file)

if __name__ == "__main__":
    add_path = "hacky_test_aleksis/"
    input_svg = add_path + 'floor_2.svg'  # Replace with your input SVG file path
    output_svg = add_path + 'output.svg'  # Replace with your desired output SVG file path
    remove_elements_from_svg(input_svg, output_svg)