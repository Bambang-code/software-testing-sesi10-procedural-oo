# Software Testing Sesi 10 - Procedural & Object Oriented Test Suite

**Bambang Herlambang - 5803024019**

Tugas individu | Informatika, Universitas Katolik Widya Mandala Surabaya

Dosen: Philipus Suryo Subandoro

Studi kasus: **Auth marketplace ZENTA**, disederhanakan menjadi model Python
yang dapat diuji tanpa Google, database, server, maupun kredensial.
Repo ini terpisah dari repo implementasi kelompok. Tidak perlu deploy backend.

## Hasil pengujian

Snapshot lokal 2 November 2026, Python 3.10.11:

| Pengukuran | Hasil aktual |
|---|---:|
| PyTest | 96 passed, 0 gagal/error/skip |
| Statement | 62/62 (100%) |
| Branch | 18/18 (100%) |
| Basis path fungsi utama | 4 jalur, V(G) = 4 |
| State/event matrix | 16 pasangan x 3 class = 48 kasus |

Angka dapat diverifikasi melalui [log PyTest](reports/pytest.txt),
[coverage](reports/coverage.txt), dan [metadata eksekusi](reports/run-metadata.json).
Snapshot ini adalah hasil lokal. GitHub Actions belum diaktifkan; template CI
opsional tersedia di [docs/ci-tests.yml](docs/ci-tests.yml).

## Isi tugas

1. [Fungsi prosedural](src/zenta_auth/scopes.py) dengan 3 keputusan:
   client aktif, scope tidak kosong, dan seluruh scope diizinkan.
2. [CFG, V(G), empat basis path, dan analisis data flow](docs/analysis.md#cfg).
3. [Empat test basis path serta variasi input](tests/test_scopes.py).
4. [Class OO](src/zenta_auth/seller.py): DRAFT, PENDING, APPROVED, REJECTED;
   [state machine dan tabel transisi](docs/analysis.md#state-machine-oo).
5. [Test state, inheritance, dan polymorphism](tests/test_seller.py), termasuk
   invalid transition, state tidak berubah saat gagal, dan urutan pemanggilan.
6. [Laporan LaTeX](laporan/laporan-sesi10-bambang.tex) dan
   [laporan PDF siap dibaca](output/pdf/laporan-sesi10-bambang.pdf).

## Jalankan di Windows PowerShell

```powershell
git clone https://github.com/Bambang-code/software-testing-sesi10-procedural-oo.git
cd software-testing-sesi10-procedural-oo
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe scripts/run_tests.py
Start-Process .\htmlcov\index.html
```

Tidak perlu mengaktifkan virtual environment ataupun mengubah ExecutionPolicy.
Jika repo sudah tersedia, mulai dari `cd` ke folder repo yang benar.

Untuk Linux/macOS:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/run_tests.py
```

Perintah PyTest langsung (menggunakan Python dari virtual environment):

```powershell
.\.venv\Scripts\python.exe -m pytest -v --cov=zenta_auth --cov-branch --cov-report=term-missing --cov-report=html
```

`scripts/run_tests.py` menjalankan PyTest satu kali, menyimpan bukti di `reports/`,
dan membuat `htmlcov/index.html`. Threshold coverage 100% diberlakukan untuk
model kecil ini; tidak ada `pragma: no cover` maupun pengecualian source.
Tool versi tetap tercantum di `requirements-dev.txt` (Python >= 3.10).

## Bangun ulang laporan

PDF final sudah disertakan. Untuk membangun ulang, pasang
[Tectonic](https://tectonic-typesetting.github.io/) atau gunakan LaTeX lokal.
Dengan Tectonic di PATH:

```powershell
.\.venv\Scripts\python.exe scripts/build_report.py
```

Jika binary berada di folder lain:

```powershell
.\.venv\Scripts\python.exe scripts/build_report.py --tectonic "C:\path\tectonic.exe"
```

Builder memeriksa hash source/test terhadap hasil pengujian sebelum menulis
angka coverage dan cuplikan kode pada `laporan/generated/`. Jika source berubah,
jalankan kembali `scripts/run_tests.py`. Output PDF berada di `output/pdf/`.
Untuk Overleaf, unggah folder `laporan/` beserta folder `reports/` sebagai sibling;
pilih `laporan/laporan-sesi10-bambang.tex` sebagai main document.
File generated merupakan bagian dari sumber laporan dan disertakan di repo.

## Struktur

```text
src/zenta_auth/       Kode yang diuji: scopes.py dan seller.py
tests/               Fixture, test basis path, test state dan subclass
docs/analysis.md     CFG, jalur, state machine, matriks, dan pemetaan rubrik
scripts/             Pengujian + penghasil bukti, builder laporan
reports/             Log aktual, coverage JSON/XML, JUnit, metadata dan hash
laporan/             LaTeX, logo kampus, hasil generator
output/pdf/          Laporan PDF final
docs/ci-tests.yml    Template CI opsional dengan artefak coverage
```

HTML coverage dan virtual environment diabaikan Git; keduanya dapat dibuat ulang.
CI bukan syarat Tugas Sesi 10. Login CLI saat publikasi belum memiliki scope
`workflow`, sehingga file CI disertakan sebagai template yang belum aktif.
Untuk mengaktifkannya nanti, simpan isi `docs/ci-tests.yml` sebagai
`.github/workflows/tests.yml` melalui editor GitHub atau login CLI dengan izin
workflow. Setelah commit, periksa tab
[Actions](https://github.com/Bambang-code/software-testing-sesi10-procedural-oo/actions).
Template menjalankan tes dan mengunggah laporan sebagai artefak, tanpa deploy.

## Batas interpretasi

- `validate_scopes` adalah pemeriksaan izin setelah verifikasi identitas client,
  bukan implementasi OAuth/JWT lengkap.
- DRAFT, withdraw, kategori GENERAL, dan subclass adalah model pembelajaran;
  tidak mengubah requirements/architecture atau hak akses ZENTA kelompok.
- Semua 16 pasangan state/event diuji pada tiga implementasi, tetapi coverage
  100% tidak menjamin seluruh input atau semua urutan tak terbatas benar.
- Coverage hanya mencakup `src/zenta_auth`, bukan test, tooling, frontend,
  Google, atau layanan ZENTA produksi.
- Logo kampus digunakan sebagai identitas akademik laporan, bukan logo ZENTA.

## Referensi

- Materi Software Testing Sesi 10, Philipus Suryo Subandoro, sesuai teks tugas mahasiswa.
- [PyTest parametrization](https://docs.pytest.org/en/stable/how-to/parametrize.html).
- [pytest-cov --cov-branch](https://pytest-cov.readthedocs.io/en/latest/config.html).
- [coverage.py branch measurement](https://coverage.readthedocs.io/en/latest/branch.html).
- McCabe, T. J. (1976). A Complexity Measure. IEEE TSE, SE-2(4), 308-320.
  DOI: 10.1109/TSE.1976.233837.
