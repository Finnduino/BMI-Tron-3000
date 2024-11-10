import fitz  # PyMuPDF

def remove_lines_from_pdf(input_file, output_file):
    doc = fitz.open(input_file)
    
    for page in doc:
        # Get all drawing commands
        drawings = page.get_drawings()
        
        # Print all drawing commands for debugging
        # print(f"Page {page.number}: {drawings}")
        
        # Filter out line drawings
        filtered_drawings = [drawing for drawing in drawings if not (drawing['type'] == 's' and all(item[0] == 'l' for item in drawing['items']))]
        
        # Clear the page contents
        page.clean_contents()
        
        # Recreate the page content without the lines
        for drawing in filtered_drawings:
            if drawing['type'] == 's':
                for item in drawing['items']:
                    if item[0] == 'l':
                        page.draw_line(item[1], item[2], color=drawing['color'], width=drawing['width'])
                    # Add handling for other drawing types if needed
            elif drawing['type'] == 'f':
                # Ensure width and fill are not None
                width = drawing['width'] if drawing['width'] is not None else 1.0
                fill = drawing['fill'] if drawing['fill'] is not None else (0, 0, 0)
                page.draw_rect(drawing['rect'], color=fill, fill=fill, width=width)
            # Add handling for other drawing types if needed
    
    # Save the modified PDF to the output file
    doc.save(output_file)

if __name__ == "__main__":
    add_path = "hacky_test_aleksis/"
    input_pdf =  add_path + 'floor_1.pdf'  # Replace with your input PDF file path
    output_pdf = add_path +  'output.pdf'  # Replace with your desired output PDF file path
    remove_lines_from_pdf(input_pdf, output_pdf)