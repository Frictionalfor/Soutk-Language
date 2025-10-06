import qrcode

data = "https://leetcode.com/u/frictional_for/"
qr_img = qrcode.make(data)
qr_img.save("soutk_qr.png")

print("QR code generated and saved as soutk_qr.png")