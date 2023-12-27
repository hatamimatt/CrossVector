import ezdxf

def create_drawing(length, width, filename="output.dxf"):
    doc = ezdxf.new("R2007")  # Use the DXF R2007 format

    msp = doc.modelspace()
    points = [(0, 0), (length, 0), (length, width), (0, width)]
    msp.add_lwpolyline(points, is_closed=True)

    doc.saveas(filename)

    print(f"Drawing created successfully: {filename}")

# Example: Create a drawing with dimensions 10x8 units
create_drawing(10, 8)