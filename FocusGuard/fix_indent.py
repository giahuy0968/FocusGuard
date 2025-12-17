"""
Script tự động sửa lỗi indent cho hàm show_rest_stops_map trong Runner.py
"""

def fix_indentation():
    with open('Runner.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find start and end of function
    start_line = None
    end_line = None
    
    for i, line in enumerate(lines):
        if line.strip().startswith('def show_rest_stops_map():'):
            start_line = i
        if start_line is not None and line.strip().startswith('def format_label('):
            end_line = i
            break
    
    if start_line is None:
        print("Không tìm thấy hàm show_rest_stops_map")
        return
    
    print(f"Tìm thấy hàm từ dòng {start_line + 1} đến {end_line}")
    
    # Fix indentation
    fixed_lines = []
    in_try_block = False
    
    for i in range(start_line, end_line):
        line = lines[i]
        
        # Keep function definition
        if 'def show_rest_stops_map():' in line:
            fixed_lines.append(line)
            continue
        
        # Keep docstring
        if '"""' in line and not in_try_block:
            fixed_lines.append(line)
            continue
        
        # Handle try block
        if line.strip().startswith('try:'):
            fixed_lines.append(line)
            in_try_block = True
            continue
        
        # Handle except block
        if line.strip().startswith('except'):
            in_try_block = False
            fixed_lines.append(line)
            continue
        
        # Fix indentation for lines in try block
        if in_try_block:
            # Remove leading spaces and add correct indent (8 spaces = 2 levels)
            content = line.lstrip()
            if content and not content.startswith('#'):
                # Lines that should have 8 spaces (in try block)
                if content.startswith(('map_window', 'window_', 'screen_', 'x =', 'y =')) or \
                   content.startswith(('header_', 'title_', 'subtitle_', 'input_', 'location_', 
                                      'search_', 'radius_', 'facility_', 'results_', 'tree',
                                      'scrollbar', 'status_', 'def ', 'button_')):
                    fixed_lines.append('        ' + content)
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    # Write back
    new_content = ''.join(lines[:start_line]) + ''.join(fixed_lines) + ''.join(lines[end_line:])
    
    with open('Runner.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Đã sửa {len(fixed_lines)} dòng")
    print("Vui lòng kiểm tra lại file Runner.py")

if __name__ == "__main__":
    fix_indentation()
