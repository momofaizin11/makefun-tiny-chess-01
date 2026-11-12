# NOTES - main.py (4053 byte, stdlib, satu file)

Papan: 10x12 ber-border '#', indeks=(rank+2)*10+file+1, geseran bidak
cukup satu angka (1,-1,10,-10,11,9,-11,-9) tanpa cek tepi. State =
(papan,sisi,ep); hak castling dibaca dari papan, bukan dibukukan.

Movegen: pseudo-legal dimainkan di salinan papan, legal bila raja
sendiri tidak diserang (attack test). Promosi q/r/b/n, en passant,
castling (petak lintasan dicek) benar.

Cari: negamax alpha-beta + iterative deepening 1..11, budget node
TETAP 60000/langkah (NB), bukan jam: lewat budget = exception, pakai
hasil kedalaman terakhir yang selesai. Quiescence makan/promosi/ep +
stand-pat. Urutan langkah MVV-LVA + nilai promosi.

Eval: material p100 n320 b330 r500 q900, bidak maju +8/baris, kuda n
menteri dekat pusat, raja di baris rumah, bishop pair +30, bidak dobel
-12.

Root: legal_moves env = himpunan sah, dinilai pencarian sendiri.

Determinisme: tanpa jam/acak -> posisi+budget sama = langkah sama.

Validasi: perft 20/400/8902/197281, 48/2039/97862, 14/191/2812/43238,
2 posisi CPW lain, dicocokkan langkah-per-langkah dengan generator
referensi independen di luar repo; protokol diuji ke server tiruan.
