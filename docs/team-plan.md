# Team Plan — PulseUP (Kelompok 2)

Mata kuliah: ISP132 Pemrograman Berorientasi Objek, Universitas Jambi.
Repositori: https://github.com/cow-907/Tugas-Akhir---PBO

## Tujuan

Aplikasi web pemantauan kesehatan startup: menilai tiga metrik (keuangan, produk,
pengguna) menjadi status SEHAT, WASPADA, atau KRITIS beserta rekomendasinya.

## Lingkup

Termasuk: pemilihan peran, identifikasi tim, input data bulanan, validasi,
evaluasi, rekap dan filter untuk mentor, antarmuka web Flask.

Di luar lingkup: database, login, riwayat antarbulan, dan data lebih dari satu
bulan berjalan.

## Peran

| Anggota | Peran | Berkas yang dipegang |
| --- | --- | --- |
| Selvy Amanda Saputri | Ketua, desain class dan SOLID, review kode | `metrik.py`, `uji_web.py` |
| M. Akmal Faizhin Hafiz | Backend domain dan rute Flask | `tim_startup.py`, `penilai.py`, `app.py` |
| Salma Mahira | Pengujian dan template halaman | `mentor.py`, `data_tim.py`, `uji_class.py`, `templates/` |
| Rionza | Pemilik repositori, dokumentasi, integrasi | `adaptor_form.py`, `uji_adaptor.py`, `static/`, `README.md`, `docs/`, `.github/` |

## Kesepakatan kerja

- Satu issue, satu branch, satu pull request. Nama branch: `feat/<nomor>-<ringkasan>`.
- Maksimal dua kartu di kolom In Progress untuk seluruh tim.
- Setiap anggota commit dari laptop dan akun GitHub masing-masing.
- Email Git harus sama dengan email akun GitHub.
- Tidak ada push langsung ke `main`; semua lewat pull request.
- Minimal satu rekan membaca diff sebelum merge.
- Pertemuan singkat tiap awal sesi, maksimal 10 menit: hasil kemarin, rencana
  hari ini, hambatan.

## Awalan pesan commit

`feat:` fitur baru · `fix:` perbaikan · `test:` pengujian · `docs:` dokumentasi ·
`chore:` pekerjaan penunjang. Sertakan nomor issue, misalnya
`feat: form input data metrik (#9)`.

## Definition of Done

- [ ] Kriteria penerimaan pada issue terpenuhi.
- [ ] Seluruh uji dijalankan dan hasil aktualnya dicatat di pull request.
- [ ] Satu rekan sudah membaca diff dan menyetujui.
- [ ] Tidak ada `.venv`, `__pycache__`, atau kata sandi yang ikut ter-commit.
- [ ] Pull request sudah di-merge ke `main`.
- [ ] Kartu dipindahkan ke Done.

## Papan Kanban

GitHub Projects, papan `PulseUP Project`, dengan kolom Backlog, Ready,
In Progress, Review, dan Done. Field tambahan: Priority, Estimate, Target date.
