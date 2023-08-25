1. Script ini untuk membuat jalurterbang Spraying untuk drone spraying FC JIYI.
2. Data yang dihasilkan adalah berupa garis(.shp).
3. Data garis/polyline(.shp) yang diperlukan menggunakan koordinat "WGS_1984", mohon tidak diproject atau menggunakan koordinat UTM seperti 48 S, 49 S,48 N, dan lain-lain.
4. Bila menggunakan data DSM(.tif) boleh menggunakan koordinat WGS_1984, maupun koordinat UTM.


Data tersebut dilanjutkan di software Qgis, untuk diconvert menjadi (.kml), lalu di "dissolve".
Data hasil dissolve dapat digunakan dalam aplikasi "AgriAsistant"

Install
pip install avirtech_spraying_jiyi_lib

Usage
from avirtech_spraying_jiyi_lib.avirtech_spraying_jiyi import autocorrect