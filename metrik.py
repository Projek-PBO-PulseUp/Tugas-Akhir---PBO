"""
metrik.py
Enumerasi Status dan hierarki class Metrik untuk PulseUP (Milestone 2).

Isi file:
- Status              : enumerasi tingkat kesehatan (SEHAT < WASPADA < KRITIS)
- DataTidakValidError : error untuk data masukan yang tidak valid
- Metrik              : class induk abstrak
- MetrikKeuangan, MetrikProduk, MetrikPengguna : subclass konkret
"""
import math
from abc import ABC, abstractmethod
from enum import IntEnum


class Status(IntEnum):
    """Tingkat kesehatan. Nilai yang lebih besar berarti kondisi lebih buruk."""
    SEHAT = 1
    WASPADA = 2
    KRITIS = 3


class DataTidakValidError(ValueError):
    """Dilempar saat data masukan metrik tidak valid."""


def _ke_angka(nilai, nama_kolom, bulat=False, harus_positif=False):
    """Ubah nilai (angka atau teks dari form) menjadi angka yang valid.

    Menolak: bukan angka, kosong, negatif, NaN/tak hingga, nol (jika
    harus_positif), dan bukan bilangan bulat (jika bulat=True).
    """
    if isinstance(nilai, bool):  # bool adalah subclass int, tolak secara eksplisit
        raise DataTidakValidError(f"{nama_kolom} harus berupa angka.")
    if isinstance(nilai, str):
        teks = nilai.strip().replace(",", ".")  # "2,5" -> "2.5"
        if teks == "":
            raise DataTidakValidError(f"{nama_kolom} tidak boleh kosong.")
        nilai = teks
    try:
        angka = float(nilai)
    except (TypeError, ValueError):
        raise DataTidakValidError(
            f"{nama_kolom} harus berupa angka (tanpa pemisah ribuan)."
        ) from None
    if not math.isfinite(angka):
        raise DataTidakValidError(f"{nama_kolom} harus berupa angka yang valid.")
    if angka < 0:
        raise DataTidakValidError(f"{nama_kolom} tidak boleh negatif.")
    if harus_positif and angka == 0:
        raise DataTidakValidError(f"{nama_kolom} harus lebih dari 0.")
    if bulat:
        if angka != int(angka):
            raise DataTidakValidError(f"{nama_kolom} harus berupa bilangan bulat.")
        return int(angka)
    return angka


class Metrik(ABC):
    """Class induk abstrak untuk semua metrik kesehatan startup.

    Subclass wajib mengimplementasikan hitung_skor(), hitung_status(), dan
    buat_rekomendasi(). PenilaiStartup hanya bergantung pada class ini
    (polimorfisme + Open/Closed Principle).
    """

    def __init__(self, nama_metrik):
        self._nama_metrik = nama_metrik
        self._skor = 0.0
        self._status = None

    @property
    def nama_metrik(self):
        return self._nama_metrik

    @property
    def skor(self):
        """Skor terakhir yang dihitung (0-100)."""
        return self._skor

    @property
    def status(self):
        """Status terakhir yang dihitung (None bila belum dihitung)."""
        return self._status

    @abstractmethod
    def hitung_skor(self):
        """Hitung dan kembalikan skor 0-100 (dibulatkan 1 desimal)."""

    @abstractmethod
    def hitung_status(self):
        """Hitung dan kembalikan Status (SEHAT/WASPADA/KRITIS)."""

    @abstractmethod
    def buat_rekomendasi(self):
        """Kembalikan satu kalimat rekomendasi sesuai status saat ini."""

    @staticmethod
    def _tentukan_status(nilai, ambang_sehat, ambang_waspada):
        """Pembantu: nilai >= ambang_sehat -> SEHAT, >= ambang_waspada -> WASPADA."""
        if nilai >= ambang_sehat:
            return Status.SEHAT
        if nilai >= ambang_waspada:
            return Status.WASPADA
        return Status.KRITIS


class MetrikKeuangan(Metrik):
    """Menilai ketahanan keuangan berdasarkan runway (bulan)."""

    AMBANG_SEHAT = 6      # runway >= 6 bulan   -> SEHAT
    AMBANG_WASPADA = 3    # runway 3 - <6 bulan -> WASPADA, <3 -> KRITIS

    _REKOMENDASI = {
        Status.KRITIS: "Segera kurangi pengeluaran operasional dan cari tambahan dana.",
        Status.WASPADA: "Pantau pengeluaran dan mulai siapkan rencana pendanaan berikutnya.",
        Status.SEHAT: "Kondisi keuangan sehat; pertahankan pengelolaan kas.",
    }

    def __init__(self, saldo_kas, pengeluaran_bulanan):
        super().__init__("Keuangan")
        self.saldo_kas = saldo_kas
        self.pengeluaran_bulanan = pengeluaran_bulanan
        self._runway = 0.0

    @property
    def saldo_kas(self):
        return self._saldo_kas

    @saldo_kas.setter
    def saldo_kas(self, nilai):
        self._saldo_kas = _ke_angka(nilai, "Saldo kas")

    @property
    def pengeluaran_bulanan(self):
        return self._pengeluaran_bulanan

    @pengeluaran_bulanan.setter
    def pengeluaran_bulanan(self, nilai):
        self._pengeluaran_bulanan = _ke_angka(
            nilai, "Pengeluaran bulanan", harus_positif=True
        )

    @property
    def runway(self):
        return self.hitung_runway()

    def hitung_runway(self):
        """Berapa bulan saldo kas cukup untuk menutup pengeluaran."""
        self._runway = self._saldo_kas / self._pengeluaran_bulanan
        return self._runway

    def hitung_skor(self):
        runway = self.hitung_runway()
        self._skor = round(min(runway / self.AMBANG_SEHAT, 1) * 100, 1)
        return self._skor

    def hitung_status(self):
        self._status = self._tentukan_status(
            self.hitung_runway(), self.AMBANG_SEHAT, self.AMBANG_WASPADA
        )
        return self._status

    def buat_rekomendasi(self):
        return self._REKOMENDASI[self.hitung_status()]


class MetrikProduk(Metrik):
    """Menilai perkembangan produk dari pencapaian target milestone (%)."""

    AMBANG_SEHAT = 50     # pencapaian >= 50%    -> SEHAT
    AMBANG_WASPADA = 25   # pencapaian 25 - <50% -> WASPADA, <25% -> KRITIS

    _REKOMENDASI = {
        Status.KRITIS: "Percepat pencapaian milestone; tinjau ulang prioritas dan hambatan tim.",
        Status.WASPADA: "Percepat pencapaian milestone agar tidak tertinggal dari target.",
        Status.SEHAT: "Perkembangan produk sesuai target; pertahankan ritme kerja.",
    }

    def __init__(self, target_milestone, capaian_milestone):
        super().__init__("Produk")
        self.target_milestone = target_milestone   # set target dulu
        self.capaian_milestone = capaian_milestone

    @property
    def target_milestone(self):
        return self._target_milestone

    @target_milestone.setter
    def target_milestone(self, nilai):
        baru = _ke_angka(nilai, "Target milestone", bulat=True, harus_positif=True)
        if getattr(self, "_capaian_milestone", 0) > baru:
            raise DataTidakValidError("Capaian milestone tidak boleh melebihi target.")
        self._target_milestone = baru

    @property
    def capaian_milestone(self):
        return self._capaian_milestone

    @capaian_milestone.setter
    def capaian_milestone(self, nilai):
        baru = _ke_angka(nilai, "Capaian milestone", bulat=True)
        if baru > self._target_milestone:
            raise DataTidakValidError("Capaian milestone tidak boleh melebihi target.")
        self._capaian_milestone = baru

    def hitung_pencapaian(self):
        """Persentase milestone yang tercapai (0-100)."""
        return self._capaian_milestone * 100 / self._target_milestone

    def hitung_skor(self):
        self._skor = round(self.hitung_pencapaian(), 1)
        return self._skor

    def hitung_status(self):
        self._status = self._tentukan_status(
            self.hitung_pencapaian(), self.AMBANG_SEHAT, self.AMBANG_WASPADA
        )
        return self._status

    def buat_rekomendasi(self):
        return self._REKOMENDASI[self.hitung_status()]


class MetrikPengguna(Metrik):
    """Menilai pertumbuhan pengguna terhadap target pengguna (%)."""

    AMBANG_SEHAT = 80     # pencapaian >= 80%    -> SEHAT
    AMBANG_WASPADA = 50   # pencapaian 50 - <80% -> WASPADA, <50% -> KRITIS

    _REKOMENDASI = {
        Status.KRITIS: "Tingkatkan upaya akuisisi pengguna; evaluasi saluran pemasaran dan nilai produk.",
        Status.WASPADA: "Tingkatkan upaya akuisisi pengguna agar mendekati target.",
        Status.SEHAT: "Pertumbuhan pengguna sesuai target; jaga retensi pengguna.",
    }

    def __init__(self, jumlah_pengguna, target_pengguna):
        super().__init__("Pengguna")
        self.jumlah_pengguna = jumlah_pengguna
        self.target_pengguna = target_pengguna

    @property
    def jumlah_pengguna(self):
        return self._jumlah_pengguna

    @jumlah_pengguna.setter
    def jumlah_pengguna(self, nilai):
        self._jumlah_pengguna = _ke_angka(nilai, "Jumlah pengguna", bulat=True)

    @property
    def target_pengguna(self):
        return self._target_pengguna

    @target_pengguna.setter
    def target_pengguna(self, nilai):
        self._target_pengguna = _ke_angka(
            nilai, "Target pengguna", bulat=True, harus_positif=True
        )

    def hitung_pencapaian(self):
        """Persentase pencapaian target (boleh lebih dari 100)."""
        return self._jumlah_pengguna * 100 / self._target_pengguna

    def hitung_skor(self):
        self._skor = round(min(self.hitung_pencapaian(), 100), 1)
        return self._skor

    def hitung_status(self):
        self._status = self._tentukan_status(
            self.hitung_pencapaian(), self.AMBANG_SEHAT, self.AMBANG_WASPADA
        )
        return self._status

    def buat_rekomendasi(self):
        return self._REKOMENDASI[self.hitung_status()]
