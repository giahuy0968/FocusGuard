"""
Script test chức năng bản đồ
"""
import tkinter as tk
from tkinter import messagebox

def test_basic():
    """Test cơ bản xem tkinter có hoạt động không"""
    try:
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Test", "Tkinter hoạt động bình thường!")
        root.destroy()
        print("✅ Test 1 PASSED: Tkinter OK")
        return True
    except Exception as e:
        print(f"❌ Test 1 FAILED: {e}")
        return False

def test_import_api():
    """Test import module API"""
    try:
        from rest_stops_api import rest_stops_finder
        print("✅ Test 2 PASSED: Module rest_stops_api import thành công")
        return True
    except ImportError as e:
        print(f"⚠️ Test 2 WARNING: Không thể import rest_stops_api - {e}")
        print("   Ứng dụng vẫn chạy được với dữ liệu mẫu")
        return False

def test_geocoding():
    """Test chức năng geocoding"""
    try:
        from rest_stops_api import rest_stops_finder
        lat, lon = rest_stops_finder.geocode_address("Hanoi, Vietnam")
        if lat and lon:
            print(f"✅ Test 3 PASSED: Geocoding OK - Hanoi tại ({lat}, {lon})")
            return True
        else:
            print("⚠️ Test 3 WARNING: Không tìm được tọa độ")
            return False
    except Exception as e:
        print(f"❌ Test 3 FAILED: {e}")
        return False

def test_sample_data():
    """Test dữ liệu mẫu"""
    try:
        from rest_stops_api import rest_stops_finder
        data = rest_stops_finder.get_sample_data("Hà Nội")
        if data:
            print(f"✅ Test 4 PASSED: Dữ liệu mẫu OK - {len(data)} địa điểm")
            for place in data[:3]:
                print(f"   - {place['name']} ({place['distance']})")
            return True
        else:
            print("❌ Test 4 FAILED: Không có dữ liệu mẫu")
            return False
    except Exception as e:
        print(f"❌ Test 4 FAILED: {e}")
        return False

def test_main_app():
    """Test mở ứng dụng chính"""
    try:
        import Runner
        print("✅ Test 5 PASSED: Module Runner import thành công")
        return True
    except Exception as e:
        print(f"❌ Test 5 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🔍 BẮT ĐẦU KIỂM TRA CHỨC NĂNG BẢN ĐỒ")
    print("=" * 60)
    print()
    
    results = []
    results.append(("Tkinter", test_basic()))
    results.append(("Import API Module", test_import_api()))
    results.append(("Geocoding", test_geocoding()))
    results.append(("Sample Data", test_sample_data()))
    results.append(("Main App", test_main_app()))
    
    print()
    print("=" * 60)
    print("📊 KẾT QUẢ KIỂM TRA")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print()
    print(f"Tổng kết: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 TẤT CẢ TESTS ĐỀU PASS! Ứng dụng sẵn sàng sử dụng!")
    elif passed >= total - 1:
        print("⚠️ Hầu hết tests pass. Ứng dụng có thể chạy với một số hạn chế.")
    else:
        print("❌ Có nhiều lỗi. Vui lòng kiểm tra lại cài đặt.")
