# NOTES - main.py (4073 byte, stdlib, satu file)

main.py = satu baris komentar versi + dua baris stdlib yang membuka payload
lzma+base85 lalu exec sumbernya (pola packing sunfish; sumber penuh
disimpan di luar repo, /root/chess4k-dev/v8.py).

Papan 10x12 ber-border. State = (papan, sisi, ep, hak castling, raja
putih, raja hitam, setengah-langkah, material non-pion). Movegen
pseudo-legal difilter uji serangan; promosi q/r/b/n, en passant,
castling dengan hak dilacak dan petak lintasan diperiksa.

Cari: negamax alpha-beta + transposition table (kunci = papan+giliran+
ep+hak), iterative deepening 1.. sampai budget node habis, PVS, null
move (R=2, hanya bila material non-pion > 1300), LMR (langkah tenang n>3:
-1 ply, n>8: -2 ply), killer + history heuristic, quiescence (hanya
makan/promosi + evasi skak, stand-pat, delta pruning). Budget 100.000 node
per langkah, bukan jam -> sama untuk masukan sama. Skakmat = M-ply;
repetisi 3x dan 50 langkah = 0; riwayat posisi game disemai dari tiap
jawaban /game dan /move.

Eval tapered: material + PST (digenerate runtime, gaya house engine) +
raja midgame/endgame, bishop pair, pion bebas.

Dibuang karena byte: PST literal ala Michniewski, tabel precompute
eval, pion dobel/terisolasi, bonus hak castling, riwayat H() replay.

Validasi: perft 20/400/8902/197281, 48/2039/97862/4085603,
14/191/2812/43238, 6/264/9467/422333, 44/1486/62379, 46/2079/89890;
5.587 posisi dari game acak dicocokkan langkah-per-langkah dengan
generator referensi independen di luar repo; simetri eval 200 posisi;
pencarian d=1..6 tanpa exception; protokol diuji ke env lokal.

Arena lokal: 4,5/6 = 75% lawan depth-3+depth-4+nodes-100k (depth-3
2-0, depth-4 1-1, nodes-100k 1-1). 181 langkah nyata: median 0,84 s,
maks 1,26 s. Budget 200.000 node dicoba: 1,5/4, waktu 2x, dibalikkan.

v3 = satu perubahan pada v2: LMR langkah tenang n>8 dipotong 2 ply (dulu
semua n>3 hanya 1 ply, re-search d-1 tetap). Budget node tetap, jadi node
yang sama menggarap garis utama -> iterative deepening sampai ply lebih
dalam.

Uji v3: perft lama dijalankan ulang, semua sama (20/400/8902/197281,
48/2039/97862, 14/191/2812/43238, 6/264/9467/422333, 44/1486/62379).
Bench 8 posisi @100.000 node: kedalaman [7,7,7,6,7,7,8,7] vs v7
[7,6,7,6,7,6,7,7] (3/8 lebih dalam, tidak pernah lebih dangkal, 7/8
langkah sama, 9,7 s vs 11,1 s). Match langsung vs v7 (24 game @20.000
node, 12 pembuka kit, warna ditukar): 12-12 (W9 D6 L9). Arena lokal 6
game yang sama lawan depth-3+depth-4+nodes-100k: 3,5/6, v7 4,5/6 ->
sampel terlalu kecil, bukan bukti mundur.

Dicoba lalu dibalikkan: reverse futility pruning (d<4, margin 110*d) -
bench lebih dalam 3/8 tapi arena 3,0/6 dan match v7 12,5/24 (eval
material+PST belum cukup dipercaya untuk pruning statis). Null move R=3
saat d>5: kedalaman sama sekali tidak berubah pada budget ini.
