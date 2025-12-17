# File chứa hàm show_rest_stops_map đã sửa lỗi
# Copy code này vào Runner.py thay thế cho hàm cũ (từ dòng 80-320)

def show_rest_stops_map():
    """Hiển thị bản đồ các trạm dừng chân, quán cà phê, nhà hàng gần nhất"""
    try:
        map_window = Toplevel(root)
        map_window.title("🗺️ Bản Đồ Trạm Dừng Chân")
        window_width = 900
        window_height = 700

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        map_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Header
        header_frame = ttk.Frame(map_window)
        header_frame.pack(fill=X, pady=(15, 10), padx=20)
        
        title_label = ttk.Label(header_frame, text="🗺️ BẢN ĐỒ TRẠM DỪNG CHÂN", 
                               font=("Segoe UI", 18, "bold"), foreground="#c0392b")
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame, text="Tìm kiếm điểm nghỉ ngơi gần vị trí của bạn", 
                                  font=("Segoe UI", 10), foreground="#7f8c8d")
        subtitle_label.pack()

        # Location input section
        input_frame = ttk.Labelframe(map_window, text="📍 Nhập Vị Trí Của Bạn", padding=15)
        input_frame.pack(fill=X, padx=20, pady=(10, 10))

        location_label = ttk.Label(input_frame, text="Địa chỉ hoặc Tọa độ:", font=("Segoe UI", 10))
        location_label.grid(row=0, column=0, padx=10, pady=8, sticky="w")

        location_var = StringVar(value="Hà Nội, Việt Nam")
        location_entry = ttk.Entry(input_frame, textvariable=location_var, width=40, font=("Segoe UI", 10))
        location_entry.grid(row=0, column=1, padx=10, pady=8, sticky="ew")

        search_radius_label = ttk.Label(input_frame, text="Bán kính tìm kiếm (km):", font=("Segoe UI", 10))
        search_radius_label.grid(row=1, column=0, padx=10, pady=8, sticky="w")

        radius_var = StringVar(value="5")
        radius_combo = ttk.Combobox(input_frame, textvariable=radius_var, 
                                    values=["1", "2", "5", "10", "20"], width=37, state="readonly")
        radius_combo.grid(row=1, column=1, padx=10, pady=8, sticky="ew")

        facility_label = ttk.Label(input_frame, text="Loại cơ sở:", font=("Segoe UI", 10))
        facility_label.grid(row=2, column=0, padx=10, pady=8, sticky="w")

        facility_var = StringVar(value="Tất cả")
        facility_combo = ttk.Combobox(input_frame, textvariable=facility_var,
                                      values=["Tất cả", "Trạm xăng", "Quán cà phê", "Nhà hàng", "Khách sạn"],
                                      width=37, state="readonly")
        facility_combo.grid(row=2, column=1, padx=10, pady=8, sticky="ew")

        input_frame.columnconfigure(1, weight=1)

        # Results section
        results_frame = ttk.Labelframe(map_window, text="📋 Danh Sách Điểm Dừng Chân", padding=10)
        results_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))

        # Treeview for results
        tree = ttk.Treeview(results_frame, columns=("Tên", "Loại", "Địa chỉ", "Khoảng cách"), 
                           show="headings", height=15)
        tree.heading("Tên", text="🏪 Tên Địa Điểm", anchor="w")
        tree.heading("Loại", text="📌 Loại", anchor="center")
        tree.heading("Địa chỉ", text="📍 Địa Chỉ", anchor="w")
        tree.heading("Khoảng cách", text="📏 Khoảng Cách", anchor="center")
        
        tree.column("Tên", width=200, anchor="w")
        tree.column("Loại", width=100, anchor="center")
        tree.column("Địa chỉ", width=300, anchor="w")
        tree.column("Khoảng cách", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill=BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")

        status_label = ttk.Label(results_frame, text="Nhấn 'Tìm Kiếm' để xem các điểm dừng chân gần bạn", 
                                font=("Segoe UI", 10), foreground="#7f8c8d")
        status_label.pack(pady=5)

        def search_places():
            """Tìm kiếm các địa điểm gần vị trí"""
            location = location_var.get().strip()
            radius = radius_var.get()
            facility = facility_var.get()
            
            if not location:
                messagebox.showwarning("⚠️ Cảnh báo", "Vui lòng nhập địa chỉ!", parent=map_window)
                return

            # Clear previous results
            for item in tree.get_children():
                tree.delete(item)
            
            status_label.config(text="🔍 Đang tìm kiếm...", foreground="#3498db")
            map_window.update()

            try:
                filtered_places = []
                
                if API_AVAILABLE:
                    # Try to use real API
                    status_label.config(text="🌐 Đang kết nối với OpenStreetMap...", foreground="#3498db")
                    map_window.update()
                    
                    # Geocode address
                    lat, lon = rest_stops_finder.geocode_address(location)
                    
                    if lat and lon:
                        # Search for places
                        places_data = rest_stops_finder.find_rest_stops(
                            lat, lon, int(radius), facility
                        )
                        
                        if places_data:
                            filtered_places = [
                                (p['name'], p['type'], p['address'], p['distance'])
                                for p in places_data
                            ]
                        else:
                            # Fallback to sample data
                            status_label.config(text="⚠️ Không tìm thấy, hiển thị dữ liệu mẫu", foreground="#f39c12")
                            sample_data = rest_stops_finder.get_sample_data(location)
                            filtered_places = [
                                (p['name'], p['type'], p['address'], p['distance'])
                                for p in sample_data
                                if facility == "Tất cả" or p['type'] == facility
                            ]
                    else:
                        # Geocoding failed, use sample data
                        status_label.config(text="⚠️ Không thể xác định vị trí, hiển thị dữ liệu mẫu", foreground="#f39c12")
                        sample_data = rest_stops_finder.get_sample_data(location)
                        filtered_places = [
                            (p['name'], p['type'], p['address'], p['distance'])
                            for p in sample_data
                            if facility == "Tất cả" or p['type'] == facility
                        ]
                else:
                    # Use sample data when API not available
                    sample_places = [
                        ("Trạm xăng Petrolimex", "Trạm xăng", "123 Đường ABC, Hà Nội", "1.2 km"),
                        ("Highlands Coffee", "Quán cà phê", "456 Đường DEF, Hà Nội", "2.5 km"),
                        ("Nhà hàng Phở Gia Truyền", "Nhà hàng", "789 Đường GHI, Hà Nội", "3.0 km"),
                        ("Trạm xăng Shell", "Trạm xăng", "321 Đường JKL, Hà Nội", "3.5 km"),
                        ("Cà phê Trung Nguyên", "Quán cà phê", "654 Đường MNO, Hà Nội", "4.2 km"),
                        ("KFC", "Nhà hàng", "987 Đường PQR, Hà Nội", "4.8 km"),
                        ("Trạm dừng chân cao tốc", "Trạm xăng", "147 Cao tốc Hà Nội - Hải Phòng", "6.5 km"),
                        ("Khách sạn Mường Thanh", "Khách sạn", "258 Đường STU, Hà Nội", "7.2 km"),
                        ("Starbucks", "Quán cà phê", "369 Đường VWX, Hà Nội", "8.0 km"),
                        ("Nhà hàng Buffet Poseidon", "Nhà hàng", "741 Đường YZ, Hà Nội", "9.5 km"),
                    ]

                    # Filter by facility type
                    for place in sample_places:
                        if facility == "Tất cả" or place[1] == facility:
                            # Check if within radius
                            distance = float(place[3].replace(" km", ""))
                            if distance <= float(radius):
                                filtered_places.append(place)

                # Display results
                if filtered_places:
                    for idx, place in enumerate(filtered_places):
                        tag = "evenrow" if idx % 2 == 0 else "oddrow"
                        tree.insert("", "end", values=place, tags=(tag,))
                    
                    tree.tag_configure("evenrow", background="#ecf0f1")
                    tree.tag_configure("oddrow", background="#ffffff")
                    
                    status_label.config(text=f"✅ Tìm thấy {len(filtered_places)} địa điểm", foreground="#27ae60")
                else:
                    status_label.config(text="❌ Không tìm thấy địa điểm nào phù hợp", foreground="#e74c3c")

            except Exception as e:
                messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}", parent=map_window)
                status_label.config(text="❌ Lỗi khi tìm kiếm", foreground="#e74c3c")
                print(f"Search error: {e}")

        def open_in_google_maps():
            """Mở bản đồ Google Maps"""
            location = location_var.get().strip()
            if location:
                # Encode location for URL
                encoded_location = parse.quote(location)
                url = f"https://www.google.com/maps/search/rest+stops+near+{encoded_location}"
                webbrowser.open(url)
            else:
                messagebox.showwarning("⚠️ Cảnh báo", "Vui lòng nhập địa chỉ!", parent=map_window)

        def get_directions():
            """Lấy chỉ dẫn đến địa điểm được chọn"""
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("⚠️ Chú ý", "Vui lòng chọn một địa điểm!", parent=map_window)
                return
            
            item = tree.item(selected[0])
            place_name = item['values'][0]
            place_address = item['values'][2]
            
            # Open Google Maps directions
            origin = parse.quote(location_var.get().strip())
            destination = parse.quote(f"{place_name}, {place_address}")
            url = f"https://www.google.com/maps/dir/{origin}/{destination}"
            webbrowser.open(url)

        # Button frame
        button_frame = ttk.Frame(map_window)
        button_frame.pack(pady=15)

        search_btn = ttk.Button(button_frame, text="🔍 TÌM KIẾM", 
                               command=search_places, bootstyle="primary",
                               width=18)
        search_btn.grid(row=0, column=0, padx=5, ipadx=10, ipady=10)

        map_btn = ttk.Button(button_frame, text="🗺️ MỞ GOOGLE MAPS", 
                            command=open_in_google_maps, bootstyle="info-outline",
                            width=20)
        map_btn.grid(row=0, column=1, padx=5, ipadx=10, ipady=10)

        direction_btn = ttk.Button(button_frame, text="🧭 CHỈ ĐƯỜNG", 
                                  command=get_directions, bootstyle="success-outline",
                                  width=18)
        direction_btn.grid(row=0, column=2, padx=5, ipadx=10, ipady=10)

        close_btn = ttk.Button(button_frame, text="✖️ ĐÓNG", 
                              command=map_window.destroy, bootstyle="danger-outline",
                              width=12)
        close_btn.grid(row=0, column=3, padx=5, ipadx=10, ipady=10)

        # Auto search on open
        map_window.after(500, search_places)
    
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể mở bản đồ trạm dừng chân:\n{str(e)}")
        print(f"Lỗi show_rest_stops_map: {e}")
        import traceback
        traceback.print_exc()
