"""
Module để tìm kiếm trạm dừng chân, quán cà phê, nhà hàng gần vị trí
Sử dụng Nominatim API (OpenStreetMap) - miễn phí và không cần API key
"""

import requests
import json
from typing import List, Dict, Tuple
import math

class RestStopsFinder:
    def __init__(self):
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.overpass_url = "https://overpass-api.de/api/interpreter"
        self.headers = {
            'User-Agent': 'FocusGuard/1.0 (Driver Safety App)'
        }
    
    def geocode_address(self, address: str) -> Tuple[float, float]:
        """
        Chuyển đổi địa chỉ thành tọa độ (lat, lon)
        """
        try:
            params = {
                'q': address,
                'format': 'json',
                'limit': 1
            }
            response = requests.get(self.nominatim_url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    return float(data[0]['lat']), float(data[0]['lon'])
            
            return None, None
        except Exception as e:
            print(f"Lỗi geocoding: {e}")
            return None, None
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Tính khoảng cách giữa 2 điểm (km) sử dụng công thức Haversine
        """
        R = 6371  # Bán kính Trái Đất (km)
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        distance = R * c
        return round(distance, 2)
    
    def find_rest_stops(self, latitude: float, longitude: float, radius_km: int = 5, 
                       facility_type: str = "all") -> List[Dict]:
        """
        Tìm các điểm dừng chân gần vị trí
        
        Args:
            latitude: Vĩ độ
            longitude: Kinh độ
            radius_km: Bán kính tìm kiếm (km)
            facility_type: Loại cơ sở (fuel, cafe, restaurant, hotel, all)
        
        Returns:
            Danh sách các địa điểm tìm được
        """
        
        # Mapping facility types to Overpass query
        facility_mapping = {
            "Trạm xăng": "amenity=fuel",
            "Quán cà phê": "amenity=cafe",
            "Nhà hàng": "amenity=restaurant",
            "Khách sạn": "tourism=hotel",
            "Tất cả": "amenity~'fuel|cafe|restaurant|fast_food'|tourism=hotel"
        }
        
        query_filter = facility_mapping.get(facility_type, facility_mapping["Tất cả"])
        
        # Overpass QL query
        radius_meters = radius_km * 1000
        overpass_query = f"""
        [out:json][timeout:25];
        (
          node[{query_filter}](around:{radius_meters},{latitude},{longitude});
          way[{query_filter}](around:{radius_meters},{latitude},{longitude});
        );
        out body;
        >;
        out skel qt;
        """
        
        try:
            response = requests.post(self.overpass_url, data=overpass_query, 
                                   headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for element in data.get('elements', []):
                    if 'tags' in element and 'lat' in element:
                        tags = element['tags']
                        place_lat = element['lat']
                        place_lon = element['lon']
                        
                        # Determine facility type
                        place_type = "Khác"
                        if tags.get('amenity') == 'fuel':
                            place_type = "Trạm xăng"
                        elif tags.get('amenity') == 'cafe':
                            place_type = "Quán cà phê"
                        elif tags.get('amenity') in ['restaurant', 'fast_food']:
                            place_type = "Nhà hàng"
                        elif tags.get('tourism') == 'hotel':
                            place_type = "Khách sạn"
                        
                        # Get name
                        name = tags.get('name', 'Không có tên')
                        if name == 'Không có tên':
                            name = tags.get('brand', place_type)
                        
                        # Get address
                        address_parts = []
                        if 'addr:street' in tags:
                            address_parts.append(tags['addr:street'])
                        if 'addr:city' in tags:
                            address_parts.append(tags['addr:city'])
                        
                        address = ', '.join(address_parts) if address_parts else "Địa chỉ không rõ"
                        
                        # Calculate distance
                        distance = self.calculate_distance(latitude, longitude, place_lat, place_lon)
                        
                        if distance <= radius_km:
                            results.append({
                                'name': name,
                                'type': place_type,
                                'address': address,
                                'distance': f"{distance} km",
                                'latitude': place_lat,
                                'longitude': place_lon
                            })
                
                # Sort by distance
                results.sort(key=lambda x: float(x['distance'].replace(' km', '')))
                return results[:20]  # Limit to 20 results
            
            return []
        
        except Exception as e:
            print(f"Lỗi tìm kiếm: {e}")
            return []
    
    def get_sample_data(self, location_name: str = "Hà Nội") -> List[Dict]:
        """
        Trả về dữ liệu mẫu khi không có kết nối internet hoặc API lỗi
        """
        sample_data = {
            "Hà Nội": [
                {"name": "Trạm xăng Petrolimex Giải Phóng", "type": "Trạm xăng", 
                 "address": "123 Đường Giải Phóng, Hai Bà Trưng", "distance": "1.2 km",
                 "latitude": 21.0245, "longitude": 105.8412},
                {"name": "Highlands Coffee Vincom", "type": "Quán cà phê", 
                 "address": "191 Bà Triệu, Hai Bà Trưng", "distance": "2.3 km",
                 "latitude": 21.0167, "longitude": 105.8449},
                {"name": "Phở Thìn Bờ Hồ", "type": "Nhà hàng", 
                 "address": "61 Đinh Tiên Hoàng, Hoàn Kiếm", "distance": "3.5 km",
                 "latitude": 21.0285, "longitude": 105.8542},
                {"name": "Trạm xăng Shell Láng Hạ", "type": "Trạm xăng", 
                 "address": "Đường Láng, Đống Đa", "distance": "2.8 km",
                 "latitude": 21.0122, "longitude": 105.8095},
                {"name": "Cà phê Trung Nguyên Legend", "type": "Quán cà phê", 
                 "address": "26 Lê Thái Tổ, Hoàn Kiếm", "distance": "4.1 km",
                 "latitude": 21.0308, "longitude": 105.8516},
                {"name": "KFC Royal City", "type": "Nhà hàng", 
                 "address": "72A Nguyễn Trãi, Thanh Xuân", "distance": "3.2 km",
                 "latitude": 21.0013, "longitude": 105.8120},
                {"name": "Khách sạn Melia", "type": "Khách sạn", 
                 "address": "44B Lý Thường Kiệt, Hoàn Kiếm", "distance": "5.5 km",
                 "latitude": 21.0212, "longitude": 105.8381},
            ],
            "Hồ Chí Minh": [
                {"name": "Trạm xăng Petrolimex Võ Văn Kiệt", "type": "Trạm xăng", 
                 "address": "123 Võ Văn Kiệt, Quận 1", "distance": "1.5 km",
                 "latitude": 10.7626, "longitude": 106.6817},
                {"name": "The Coffee House Nguyễn Huệ", "type": "Quán cà phê", 
                 "address": "Đường Nguyễn Huệ, Quận 1", "distance": "2.0 km",
                 "latitude": 10.7744, "longitude": 106.7025},
                {"name": "Phở Hòa Pasteur", "type": "Nhà hàng", 
                 "address": "Đường Pasteur, Quận 1", "distance": "2.5 km",
                 "latitude": 10.7832, "longitude": 106.6978},
            ]
        }
        
        # Return data for matching city or default to Hanoi
        for city, data in sample_data.items():
            if city.lower() in location_name.lower():
                return data
        
        return sample_data["Hà Nội"]

# Singleton instance
rest_stops_finder = RestStopsFinder()
