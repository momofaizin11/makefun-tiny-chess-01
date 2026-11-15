# NOTES - main.py (4087 byte, stdlib, satu file)

main.py = komentar versi + stdlib yang membuka payload lzma+base85 lalu
exec sumbernya (pola packing sunfish; sumber penuh di /root/chess4k-dev/v8.py).

Papan 10x12 ber-border. State = (papan, sisi, ep, hak castling, raja putih,
raja hitam, setengah-langkah, material non-pion). Movegen pseudo-legal difilter
uji serangan; promosi q/r/b/n, en passant, castling dengan hak dilacak.

Cari: negamax alpha-beta + transposition table (kunci = papan+giliran+ep+hak),
iterative deepening sampai budget node habis (100.000, bukan jam -> determinis),
PVS, null move (R=2, bila material non-pion > 1300), LMR (tenang n>3: -1 ply,
n>8: -2 ply), killer + history, quiescence (makan/promosi + evasi skak,
stand-pat, delta pruning). Skakmat = M-ply; repetisi 3x dan 50 langkah = 0;
riwayat posisi disemai dari tiap jawaban /game dan /move.

Eval tapered: material + PST (digenerate runtime, gaya house engine) + raja
midgame/endgame, bishop pair, pion bebas; v11: bonus benteng di file pion
terbuka/half-open (+12/+6) dari peta file pion di awal evaluasi (uji internal
8 partai, anchor panitia: ~1.355 poin, naik dari ~1.188).

Dibuang karena byte: PST literal Michniewski, tabel precompute, pion dobel/
terisolasi, bonus castling, riwayat H() replay. Dicoba lalu dibalikkan:
reverse futility pruning (arena & match vs v7 mundur), null move R=3 (nihil).

Validasi: perft 20/400/8902/197281, 48/2039/97862/4085603, 14/191/2812/43238,
6/264/9467/422333, 44/1486/62379, 46/2079/89890; 5.587 posisi game acak
dicocokkan langkah-per-langkah dengan generator referensi independen; simetri
eval 200 posisi; pencarian d=1..6 tanpa exception; protokol diuji ke env lokal.

Arena lokal 4,5/6 = 75% lawan depth-3+depth-4+nodes-100k; 181 langkah nyata:
median 0,84 s, maks 1,26 s. Budget 200.000 node: 1,5/4, dibalikkan. v3 (LMR
n>8 -2 ply): perft ulang sama semua; bench 8 posisi @100k node kedalaman
[7,7,7,6,7,7,8,7] vs v7 [7,6,7,6,7,6,7,7]; match 24 game vs v7: 12-12.
Catatan: README.md kini memuat badge resmi panitia make.fun.
