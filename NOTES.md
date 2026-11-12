# NOTES - main.py (4061 byte, stdlib, satu file)

main.py = dua baris stdlib yang membuka payload lzma+base85 lalu exec
sumbernya (pola packing sunfish; sumber penuh disimpan di luar repo).

Papan 10x12 ber-border. State = (papan, sisi, ep, hak castling, raja
putih, raja hitam, setengah-langkah, material non-pion). Movegen
pseudo-legal difilter uji serangan; promosi q/r/b/n, en passant,
castling dengan hak dilacak dan petak lintasan diperiksa.

Cari: negamax alpha-beta + transposition table (kunci = papan+giliran+
ep+hak), iterative deepening 1.. sampai budget node habis, PVS, null
move (R=2, hanya bila material non-pion > 1300), LMR, killer + history
heuristic, quiescence (hanya makan/promosi + evasi skak, stand-pat,
delta pruning). Budget 100.000 node per langkah, bukan jam -> sama
untuk masukan sama. Skakmat = M-ply; repetisi 3x dan 50 langkah = 0;
riwayat posisi game disemai dari tiap jawaban /game dan /move.

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
