import gspread
from oauth2client.service_account import ServiceAccountCredentials
#pip install gspread oauth2client
# KẾT NỐI GOOGLE SHEET
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
] 
confirms = ServiceAccountCredentials.from_json_keyfile_name("project-python-ggsheet-70ea12c701b2.json", scope)
bridge= gspread.authorize(confirms)  #cấp quyền 

sheet_name = "projectpython"   # Tên Sheet
sh = bridge.open(sheet_name)
ws = sh.worksheet("nhậplieu")
ws2=sh.worksheet("thongke")



# 1. THÊM HÀNG HÓA
def them_hh():
    stt = input("Số thứ tự: ")
    mahh = input("Mã hàng hóa: ")
    ten = input("Tên hàng hóa: ")
    nsd = input("Ngày sản xuất: ")
    hsd = input("Hạn sử dụng: ")
    so_luong = int(input("Số lượng nhập: "))
    xuat_xu = input("Xuất xứ: ")
    ma_nguon = input("Mã nguồn gốc: ")
    gia_goc = int(input("Giá gốc: "))
    gia_ban = int(input("Giá bán: "))
    tienloi=int(gia_ban-gia_goc)
    # số lượng đã bán mặc định = 0
    ws.append_row([stt, mahh, ten, nsd, hsd, so_luong,
                   xuat_xu, ma_nguon, 0, gia_goc, gia_ban,tienloi])
    print("stt__mahh__ten__nsd__hsd__soluong__xuatxu__manguon__gia goc__giaban")
    print(stt, mahh, ten, nsd, hsd, so_luong, xuat_xu, ma_nguon, gia_goc, gia_ban )

    print("Thêm hàng thành công!\n")



# 2. HIỂN THỊ & CẬP NHẬT SỐ LƯỢNG BÁN
def hien_thi_and_cap_nhat():
    #hiển thị 
    data = ws.get_all_values()

    print("===== DANH SÁCH HÀNG HÓA =====")
   

    for row in data[2:]:
        print("Mã | Tên | SL | Đã bán")
        print(row[1], "|", row[2], "|", row[5], "|", row[8])

    # cập nhật 
    
    
    for solan in range(1,6):

        cap = input(f"\nNhập mã hàng muốn cập nhật({solan}): ")

        for i, row in enumerate(data[2:], start=3):
            if row[1] == cap:
                ten = row[2]
                sl = int(row[5])
                da_ban = int(row[8])

                print("==> Tìm thấy:", ten)
                so_mua = int(input("Nhập số lượng mua: "))

                if so_mua > (sl - da_ban):
                    print(" Không đủ hàng trong kho!")
                    return
                    
                ws.update_cell(i, 9, da_ban + so_mua)
                print(" Cập nhật thành công!")
                print(f"""san phẩm sau khi thêm:
                            tên:{ten}
                            số lượng đã bán:{da_ban+so_mua} sản phẩm
                            só lượng còn lại:{sl-(da_ban+so_mua)} sản phẩm""")
                break
        else:
            print(" Không tìm thấy mã hàng!") 
        break
    else:
        print("bạn đã nhập quá 5 lần--->yêu cầu không thành công. ")           
        return
    
                



# 3. SẢN PHẨM HẾT HÀNG

def san_pham_da_het_hang():
    #hiển thị sản phẩm hết hàng
    data = ws.get_all_values()

    print("===== SẢN PHẨM HẾT HÀNG =====")
    for row in data[2:]:
        ten = row[2]
        stt=row[0]
        sl = int(row[5])
        da_ban = int(row[8])

        if sl - da_ban <= 0:
            print(f" {stt} :{ten}--> sản phẩm đã hết hàng")

     #cập nhật
    
    capnhat=input("bạn có muốn cập nhật số lượng không:(1:có/2:không)\n Lựa chọn là:")  
    if capnhat=="1":
        for solan in range(1,6):
            sttsp=input("sản phẩm muốn cập nhật(stt):")
            for j, row in enumerate(data[2:], start=3):
                if sttsp==row[0]:
                    ten = row[2]
                    stt=row[0]
                    sl = int(row[5])
                    slda_ban=int(row[8])
                    print(f"bạn muốn cập nhật {stt}---{ten}")
                    them=int(input("cập nhật số lượng thêm:"))
                    ws.update_cell(j, 6, sl + them)
                    print(f"cập nhật:{ten}-->soluong:{sl+them} sản phẩm,số lượng đã bán:{slda_ban}sản phẩm===>số lượng còn lại: {sl+them-slda_ban}sản phẩm")
                    print("-----cập nhật thành công------")
                    break
            else:
                print("stt không hợp lệ\nyêu cầu nhập lại")
            break
    else:
        print("lựa chọn của bạn là không cập nhật")
        return

    

    print("===============================\n")


def loi_nhuan():
    data = ws.get_all_values()       #ghi chú: lntt:lợi nhuận thực tế , lnut:lợi nhuaan ước tính , ut:ước tính , tt:thực tế .
    data2=ws2.get_all_values()
    sum=0
    doanh_thu_ut=0   #Doanh Thu ước tính
    chi_phi=0
    chiphi_spdb=0 # chi phí số phẩm đã bán
    doanh_thu_tt=0
    for row in data[2:]:
        ten=row[2]
        da_ban = int(row[8])
        gia_goc = int(row[9])
        gia_ban = int(row[10])
        sl=int(row[5])
        sum+=(gia_ban - gia_goc) * da_ban
        chi_phi+=(gia_goc*sl)
        chiphi_spdb+=(gia_goc*da_ban)
        doanh_thu_ut+=(sl*gia_ban)
        doanh_thu_tt+=(da_ban*gia_ban)
        print(f" lợi nhuận đã bán được của {ten} là: {(gia_ban - gia_goc) * da_ban} VND\n")
    print(f"""tổng chi phí phải bỏ ra để nhập sản phẩm là:{chi_phi}VND\nDoanh thu ước tính là:{doanh_thu_ut}\nLợi nhuận tổng tất cả các sản phẩm đã bán là:{sum}VND\n""")

    # thêm bảng thống kê
    print("bạn có muốn cập nhật chi phí , lợi nhuận vào bảng thống kê hay không\n 1: có \n 2:Không ")
    choose=input()
    if choose=="1":
        year=int(input("Nhập năm:"))
        lnut=doanh_thu_ut-chi_phi
        lntt=sum
        nhan_xet=input("lời nhận xét trong năm qua:")
        ws2.append_row([year,chi_phi,chiphi_spdb,doanh_thu_ut,doanh_thu_tt,lnut,lntt,nhan_xet])
        print("Cập Nhật Thành Công")
    else:
        print("bạn không muốn thêm vì chưa bán hết hàng hoặc chưa hết năm")
                                                                                                                              
        

    
def sap_het_hang():
    data = ws.get_all_values()

    print("===== SẢN PHẨM SẮP HẾT (<=5 SP) =====")
    for row in data[2:]:
        stt=row[0]
        ten = row[2]
        sl = int(row[5])
        da_ban = int(row[8])
        con_lai = sl - da_ban
        if 0 < con_lai <= 10:
            print(f"{stt} {ten}: còn {con_lai}")


    capnhat=input("bạn có muốn cập nhật số lượng không:(1:không/2:có)\n Lựa chọn là:")
    if capnhat=="2":
        for i in range(1,6):
            sttsp=input("sản phẩm muốn cập nhật:")
            for j, row in enumerate(data[2:], start=3):
                if sttsp==row[0]:
                    ten = row[2]
                    stt=row[0]
                    sl = int(row[5])
                    print(f"bạn muốn cập nhật {stt}---{ten}")
                    them=int(input("cập nhật số lượng thêm:"))
                    ws.update_cell(j, 6, sl + them)
                    print("-----cập nhật thành công------")
                    break
            else:
                print("sản phẩm không tồn tại\nyêu cầu nhập lại")  
            break
        else:
            print("bạn đã nhập quá 5 lần ---> yêu cầu của bạn không thành công")
            return
    print("==============================\n")





print("======= QUẢN LÝ HÀNG HÓA  =======")
while True:
        print("""
    1. Thêm hàng hóa
    2. Hiển thị & cập nhật bán hàng
    3. Sản phẩm hết hàng
    4. Sản phẩm sắp hết
    5. Tính lợi nhuận và Thống kê
    6. Thoát
    """)

        choose = input("Chọn: ")

        if choose == "1":
            them_hh()
        elif choose == "2":
            hien_thi_and_cap_nhat()
        elif choose == "3":
            san_pham_da_het_hang()
        elif choose == "4":
            sap_het_hang()
        elif choose == "5":
            loi_nhuan()
        elif choose == "6":
            break
        else:
            print(" Lựa chọn không hợp lệ!")


    
    
