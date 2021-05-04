text2num = \
{
 'เริ่ม': '',
 'คำนวณให้หน่อย': '',
 'เศษ': '(',
 'เปอร์เซนต์': '/100',
 'เปอร์เซ็นต์': '/100',
 'วงเล็บเปิด': '(',
 'รูท': '(',
 'เปิดวงเล็บ': '(',
 'วงเล็บปิด': ')',
 'ปิดรูท': ')**0.5',
 'จบรูท': ')**0.5',
 'คูณ': '*',
 'บวก': '+',
 'ฐาน': ',', ##
 'ลบ': '-',
 'จุด': '.',
 'ส่วน': '/', ##
 'หาร': '/',
 'สิบ': '0',
 'ศูนย์': '0',
 'ร้อย': '00',
 'พัน': '000',
 'หมื่น': '0000',
 'แสน': '00000',
 'ล้าน': '000000',
 'เอ็ด': '1',
 'หนึ่ง': '1',
 'สอง': '2',
 'ยี่': '2',
 'สาม': '3',
 'สี่': '4',
 'ห้า': '5',
 'หก': '6',
 'เจ็ด': '7',
 'แปด': '8',
 'เก้า': '9',
 'เท่ากับ': '=',
 'ยกกำลัง': '**',
 'กำลัง': '**',
 'อี': 'math.e',
 'e': 'math.e',
 'log': 'math.log(',
 'ล็อก': 'math.log(',
 'พาย': 'math.pi',
 'pi': 'math.pi',
 'เอ็กซ์': 'x'}

#------------------------------------------------------------------------------------------------------------------

text2type = \
{
 'เริ่ม': 'op',
 'คำนวณให้หน่อย': 'op',
 'เศษ': 'op',
 'เปอร์เซนต์': 'op',
 'เปอร์เซ็นต์': 'op',
 'วงเล็บเปิด': 'op',
 'รูท': 'op',
 'เปิดวงเล็บ': 'op',
 'วงเล็บปิด': 'op',
 'ปิดรูท': 'op',
 'จบรูท': 'op',
 'คูณ': 'op',
 'บวก': 'op',
 'ฐาน': 'op_incom', ##
 'ลบ': 'op',
 'จุด': 'num',
 'ส่วน': 'op_incom', ##
 'หาร': 'op',
 'สิบ': 'place',
 'ศูนย์': 'num',
 'ร้อย': 'place',
 'พัน': 'place',
 'หมื่น': 'place',
 'แสน': 'place',
 'ล้าน': 'num',
 'เอ็ด': 'num',
 'หนึ่ง': 'num',
 'สอง': 'num',
 'ยี่': 'num',
 'สาม': 'num',
 'สี่': 'num',
 'ห้า': 'num',
 'หก': 'num',
 'เจ็ด': 'num',
 'แปด': 'num',
 'เก้า': 'num',
 'เท่ากับ': 'op',
 'ยกกำลัง': 'op',
 'กำลัง': 'op',
 'อี': 'const',
 'e': 'const',
 'log': 'op',
 'ล็อก': 'op',
 'พาย': 'const',
 'pi': 'num',
 'เอ็กซ์': 'x'}

#------------------------------------------------------------------------------------------------------------------
place_rank = \
{'ร้อย': '100',
 'พัน': '1000',
 'หมื่น': '10000',
 'แสน': '100000',
 'ล้าน': '1000000',}