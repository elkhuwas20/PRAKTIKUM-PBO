"""Versi terminal dari Permutasi & Kombinasi.html."""

from itertools import combinations, combinations_with_replacement, permutations, product
from math import comb, factorial
from typing import Callable, Iterable, Iterator, Sequence, TypeAlias


MAX_INPUT = 100
BATAS_DAFTAR = 10_000
UKURAN_HALAMAN = 50
Step: TypeAlias = tuple[str, str, list[str]]
MethodAction: TypeAlias = Callable[[], None]


def format_angka(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def faktor_menurun(high: int, low: int = 1) -> list[int]:
    return list(range(high, low - 1, -1)) if high >= low else []


def uraikan_faktorial(value: int) -> str:
    factors = faktor_menurun(value, 2)
    return " x ".join(map(str, factors)) if factors else "1"


def susun_faktor(factors: list[int]) -> str:
    return " x ".join(map(str, factors)) if factors else "1"


def langkah_perkalian(factors: list[int]) -> tuple[list[str], int]:
    if not factors:
        return ["Tidak ada faktor, sehingga perkalian kosong bernilai 1."], 1
    if len(factors) == 1:
        return [f"Hanya ada satu faktor: {factors[0]}."], factors[0]

    product = factors[0]
    lines: list[str] = []
    for factor in factors[1:]:
        next_product = product * factor
        lines.append(
            f"{format_angka(product)} x {factor} = {format_angka(next_product)}"
        )
        product = next_product
    return lines, product


def keterangan_faktorial(value: int) -> str:
    return f" Menurut definisi {value}! = 1." if value < 2 else ""


def baca_bilangan_bulat(
    prompt: str,
    *,
    minimum: int = 0,
    maximum: int = MAX_INPUT,
    default: int | None = None,
) -> int:
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            return default
        try:
            value = int(raw)
        except ValueError:
            print("Masukkan bilangan bulat tanpa koma atau desimal.")
            continue
        if value < minimum:
            print(f"Nilai minimal adalah {minimum}.")
            continue
        if value > maximum:
            print(f"Nilai maksimal adalah {maximum}.")
            continue
        return value


def baca_pilihan_ya_tidak(prompt: str, *, default: bool) -> bool:
    while True:
        raw = input(prompt).strip().lower()
        if not raw:
            return default
        if raw in {"y", "ya", "yes"}:
            return True
        if raw in {"t", "tidak", "n", "no"}:
            return False
        print("Masukkan y (ya) atau t (tidak).")


def baca_input_standar(
    *,
    defaults: tuple[int, int],
    minimum_n: int = 0,
    require_r_at_most_n: bool,
) -> tuple[int, int, list[str]]:
    n = baca_bilangan_bulat(
        f"Masukkan n [{defaults[0]}]: ",
        minimum=minimum_n,
        default=defaults[0],
    )
    while True:
        r = baca_bilangan_bulat(f"Masukkan r [{defaults[1]}]: ", default=defaults[1])
        if not require_r_at_most_n or r <= n:
            break
        print(f"Nilai r ({r}) tidak boleh lebih besar dari n ({n}).")
    unsur = baca_nama_unsur(n)
    return n, r, unsur


def baca_nama_unsur(jumlah: int) -> list[str]:
    if jumlah <= 26:
        bawaan = [chr(ord("A") + indeks) for indeks in range(jumlah)]
    else:
        bawaan = [str(indeks + 1) for indeks in range(jumlah)]

    while True:
        raw = input(
            "Masukkan nama unsur dipisahkan koma "
            f"(tekan Enter untuk {', '.join(bawaan)}): "
        ).strip()
        if not raw:
            return bawaan

        unsur = [nama.strip() for nama in raw.split(",")]
        if len(unsur) != jumlah:
            print(
                f"Jumlah nama harus tepat {jumlah}, sesuai nilai n. "
                f"Anda memasukkan {len(unsur)} nama."
            )
            continue
        if any(not nama for nama in unsur):
            print("Nama unsur tidak boleh kosong.")
            continue
        if len(set(unsur)) != len(unsur):
            print("Nama setiap unsur harus berbeda.")
            continue
        return unsur


def hasil_berlabel(hasil: Iterable[Sequence[str]]) -> Iterator[str]:
    for urutan in hasil:
        yield " ".join(urutan) if urutan else "(susunan kosong)"


def tampilkan_daftar(
    judul: str,
    hasil: Iterable[str],
    jumlah_hasil: int,
) -> None:
    batas = min(jumlah_hasil, BATAS_DAFTAR)
    iterator = iter(hasil)
    sudah_ditampilkan = 0
    ukuran_halaman = min(UKURAN_HALAMAN, batas)

    print(f"\n{judul}:")
    while sudah_ditampilkan < batas:
        awal_halaman = sudah_ditampilkan
        for _ in range(min(ukuran_halaman, batas - sudah_ditampilkan)):
            try:
                susunan = next(iterator)
            except StopIteration:
                break
            sudah_ditampilkan += 1
            print(f"{sudah_ditampilkan:>5}. {susunan}")

        print(
            f"Menampilkan {sudah_ditampilkan} dari "
            f"{format_angka(jumlah_hasil)} hasil."
        )
        if sudah_ditampilkan >= batas:
            break
        if sudah_ditampilkan == awal_halaman:
            break
        pilihan = input(
            "Tekan Enter untuk melihat berikutnya, "
            "a untuk tampilkan semua, atau s untuk lewati: "
        ).strip().lower()
        if pilihan == "s":
            break
        ukuran_halaman = (
            batas - sudah_ditampilkan if pilihan == "a" else UKURAN_HALAMAN
        )

    if jumlah_hasil > BATAS_DAFTAR:
        print(
            f"Daftar dibatasi hingga {format_angka(BATAS_DAFTAR)} "
            "hasil pertama."
        )
    if jumlah_hasil == 0:
        print("Tidak ada hasil.")


def buat_langkah_permutasi(n: int, r: int) -> tuple[int, str, list[Step]]:
    remaining = n - r
    result = factorial(n) // factorial(remaining)
    kept_factors = faktor_menurun(n, remaining + 1)
    product_lines, _ = langkah_perkalian(kept_factors)
    label = f"P({n},{r})"
    steps: list[Step] = [
        (
            "Rumus umum",
            "n adalah jumlah seluruh objek, r adalah jumlah objek yang dipilih, "
            "dan tanda faktorial (!) berarti perkalian bilangan bulat berurutan "
            "dari bilangan itu turun sampai 1.",
            ["P(n,r) = n! / (n - r)!"],
        ),
        (
            "Substitusi nilai input",
            f"Ganti n dengan {n} dan r dengan {r}, lalu hitung bagian dalam "
            f"kurung: {n} - {r} = {remaining}.",
            [
                f"{label} = {n}! / ({n} - {r})!",
                f"{label} = {n}! / {remaining}!",
            ],
        ),
        (
            "Uraikan faktorial",
            "Tulis setiap faktorial sebagai perkalian lengkap."
            + keterangan_faktorial(n)
            + keterangan_faktorial(remaining),
            [
                f"{n}! = {uraikan_faktorial(n)}",
                f"{remaining}! = {uraikan_faktorial(remaining)}",
                f"{label} = ({uraikan_faktorial(n)}) / "
                f"({uraikan_faktorial(remaining)})",
            ],
        ),
        (
            "Sederhanakan pecahan",
            (
                f"Penyebut {remaining}! sama dengan faktor terakhir pada "
                f"pembilang. Faktor yang sama dicoret."
                if remaining >= 1
                else f"Penyebut {remaining}! = 1, sehingga tidak ada faktor "
                "yang dapat dicoret dan pembilang tetap utuh."
            ),
            [
                f"{label}: {remaining}! dicoret dari pembilang dan penyebut.",
                f"{label} = {susun_faktor(kept_factors)}",
            ],
        ),
        (
            "Lakukan perkalian",
            f"Kalikan {r} faktor yang tersisa dari kiri ke kanan.",
            product_lines,
        ),
        (
            "Hasil akhir",
            f"Terdapat {format_angka(result)} susunan berbeda jika {r} elemen "
            f"dipilih dari {n} elemen yang tersedia dan urutannya diperhitungkan.",
            [],
        ),
    ]
    return result, label, steps


def buat_langkah_kombinasi(n: int, r: int) -> tuple[int, str, list[Step]]:
    remaining = n - r
    result = comb(n, r)
    numerator_factors = faktor_menurun(n, remaining + 1)
    numerator_lines, numerator_value = langkah_perkalian(numerator_factors)
    denominator_factors = faktor_menurun(r, 2)
    denominator_lines, denominator_value = langkah_perkalian(denominator_factors)
    label = f"C({n},{r})"
    steps: list[Step] = [
        (
            "Rumus umum",
            "n adalah jumlah seluruh objek, r adalah jumlah objek yang dipilih, "
            "dan faktorial (!) adalah perkalian bilangan bulat berurutan sampai "
            "1. Pada kombinasi, urutan tidak diperhitungkan.",
            ["C(n,r) = n! / (r! (n - r)!)"],
        ),
        (
            "Substitusi nilai input",
            f"Ganti n dengan {n} dan r dengan {r}, lalu hitung bagian dalam "
            f"kurung: {n} - {r} = {remaining}.",
            [
                f"{label} = {n}! / ({r}! ({n} - {r})!)",
                f"{label} = {n}! / ({r}! x {remaining}!)",
            ],
        ),
        (
            "Uraikan seluruh faktorial",
            "Tulis setiap faktorial sebagai perkalian lengkap."
            + keterangan_faktorial(n)
            + keterangan_faktorial(r)
            + keterangan_faktorial(remaining),
            [
                f"{n}! = {uraikan_faktorial(n)}",
                f"{r}! = {uraikan_faktorial(r)}",
                f"{remaining}! = {uraikan_faktorial(remaining)}",
                f"{label} = ({uraikan_faktorial(n)}) / "
                f"(({uraikan_faktorial(r)}) x "
                f"({uraikan_faktorial(remaining)}))",
            ],
        ),
        (
            "Sederhanakan faktorial",
            (
                f"Faktorial (n - r)! = {remaining}! pada penyebut sama dengan "
                "faktor terakhir pada pembilang. Faktor yang sama dicoret."
                if remaining >= 1
                else f"Karena (n - r)! = 0! = 1, tidak ada faktor yang dapat "
                f"dicoret. Pembilang tetap n! dan penyebut tetap {r}!."
            ),
            [
                f"{label}: {remaining}! dicoret dari pembilang dan penyebut.",
                f"{label} = ({susun_faktor(numerator_factors)}) / "
                f"({uraikan_faktorial(r)})",
            ],
        ),
        (
            "Hitung pembilang dan penyebut",
            "Hitung pembilang dan penyebut secara terpisah.",
            [
                "Pembilang:",
                *numerator_lines,
                f"{susun_faktor(numerator_factors)} = "
                f"{format_angka(numerator_value)}",
                "Penyebut:",
                *denominator_lines,
                f"{uraikan_faktorial(r)} = {format_angka(denominator_value)}",
            ],
        ),
        (
            "Lakukan pembagian",
            "Bagi hasil pembilang dengan hasil penyebut.",
            [
                f"{label} = {format_angka(numerator_value)} / "
                f"{format_angka(denominator_value)}",
                f"{label} = {format_angka(result)}",
            ],
        ),
        (
            "Hasil akhir",
            f"Terdapat {format_angka(result)} cara berbeda untuk memilih {r} "
            f"elemen dari {n} elemen jika urutan pemilihannya tidak diperhitungkan.",
            [],
        ),
    ]
    return result, label, steps


def buat_langkah_permutasi_berulang(
    n: int, r: int
) -> tuple[int, str, list[Step]]:
    result = n**r
    factors = [n] * r
    product_lines, _ = langkah_perkalian(factors)
    label = f"P_ulang({n},{r})"
    conclusion = (
        f"Setiap posisi memiliki {n} pilihan dan terdapat {r} posisi, sehingga "
        f"total susunan yang mungkin adalah {susun_faktor(factors)} = "
        f"{format_angka(result)}."
        if r > 0
        else "Tidak ada posisi yang diisi, sehingga terdapat tepat 1 susunan "
        "(susunan kosong)."
    )
    zero_power_note = (
        " Untuk n = 0 dan r = 0 digunakan konvensi pencacahan: ada satu "
        "susunan kosong."
        if n == 0 and r == 0
        else ""
    )
    steps: list[Step] = [
        (
            "Rumus umum",
            "n adalah banyak pilihan pada setiap posisi dan r adalah banyak "
            "posisi. Elemen boleh dipakai berulang, jadi setiap posisi selalu "
            "memiliki n pilihan. Nilai r boleh lebih besar dari n.",
            ["P_ulang(n,r) = n^r"],
        ),
        (
            "Substitusi nilai input",
            f"Ganti n dengan {n} dan r dengan {r}.",
            [f"{label} = {n}^{r}"],
        ),
        (
            "Uraikan perpangkatan",
            (
                f"Pangkat {r} berarti {n} dikalikan sebanyak {r} kali, satu "
                "faktor untuk setiap posisi."
                if r > 0
                else f"Setiap bilangan berpangkat 0 bernilai 1.{zero_power_note}"
            ),
            [f"{n}^{r} = {susun_faktor(factors)}"],
        ),
        (
            "Lakukan perkalian",
            "Kalikan faktor dari kiri ke kanan dan perhatikan nilai antaranya.",
            product_lines,
        ),
        ("Hasil akhir", conclusion, []),
    ]
    return result, label, steps


def buat_langkah_permutasi_melingkar(n: int) -> tuple[int, str, list[Step]]:
    remaining = n - 1
    result = factorial(remaining)
    factors = faktor_menurun(remaining, 1)
    product_lines, _ = langkah_perkalian(factors)
    label = f"P_melingkar({n})"
    steps: list[Step] = [
        (
            "Rumus umum",
            "n adalah jumlah objek yang disusun melingkar. Susunan yang hanya "
            "berbeda karena rotasi dianggap sama, sehingga satu objek dijadikan "
            "patokan dan sisanya (n - 1) objek disusun.",
            ["P_melingkar(n) = (n - 1)!"],
        ),
        (
            "Substitusi nilai input",
            f"Ganti n dengan {n}.",
            [f"{label} = ({n} - 1)!"],
        ),
        (
            "Hitung n - 1",
            f"{n} - 1 = {remaining}.",
            [f"{label} = {remaining}!"],
        ),
        (
            "Uraikan faktorial",
            (
                f"Menurut definisi {remaining}! = 1."
                if remaining < 2
                else f"Tulis {remaining}! sebagai perkalian lengkap."
            ),
            [f"{remaining}! = {uraikan_faktorial(remaining)}"],
        ),
        (
            "Lakukan perkalian",
            "Kalikan faktor secara bertahap.",
            product_lines,
        ),
        (
            "Hasil akhir",
            f"{n} objek yang disusun mengelilingi meja bundar menghasilkan "
            f"{format_angka(result)} susunan berbeda jika susunan yang hanya "
            "berbeda karena rotasi dianggap sama.",
            [],
        ),
    ]
    return result, label, steps


def buat_langkah_unsur_identik(
    group_counts: list[int],
) -> tuple[int, str, list[Step]]:
    total_items = sum(group_counts)
    denominator = 1
    for count in group_counts:
        denominator *= factorial(count)
    result = factorial(total_items) // denominator

    largest_index = max(range(len(group_counts)), key=group_counts.__getitem__)
    largest_count = group_counts[largest_index]
    numerator_factors = faktor_menurun(total_items, largest_count + 1)
    denominator_factors = [
        factor
        for index, count in enumerate(group_counts)
        if index != largest_index
        for factor in faktor_menurun(count, 2)
    ]
    numerator_lines, numerator_value = langkah_perkalian(numerator_factors)
    denominator_lines, denominator_value = langkah_perkalian(denominator_factors)
    denominator_expansion = " x ".join(
        f"({uraikan_faktorial(count)})" for count in group_counts
    )

    steps: list[Step] = [
        (
            "Identifikasi kelompok unsur identik",
            f"Terdapat {len(group_counts)} kelompok. Unsur dalam satu kelompok "
            "identik, sehingga menukar posisinya tidak menghasilkan susunan "
            "baru. Jumlah seluruh unsur adalah total semua kelompok.",
            [
                *(f"n{index} = {count}" for index, count in enumerate(group_counts, 1)),
                f"n = {' + '.join(map(str, group_counts))} = {total_items}",
            ],
        ),
        (
            "Rumus umum",
            "n adalah jumlah seluruh unsur dan n1, n2, ..., nk adalah jumlah "
            "unsur pada tiap kelompok identik.",
            ["P = n! / (n1! x n2! x ... x nk!)"],
        ),
        (
            "Substitusi nilai input",
            f"Ganti n dengan {total_items} dan setiap ni dengan jumlah kelompoknya.",
            [
                f"P = {total_items}! / "
                f"({' x '.join(f'{count}!' for count in group_counts)})"
            ],
        ),
        (
            "Uraikan faktorial",
            "Tulis pembilang dan setiap faktorial penyebut secara lengkap."
            + (
                " Menurut definisi 0! = 1 dan 1! = 1."
                if any(value < 2 for value in [total_items, *group_counts])
                else ""
            ),
            [
                f"{total_items}! = {uraikan_faktorial(total_items)}",
                *(
                    f"{count}! = {uraikan_faktorial(count)}"
                    for count in group_counts
                ),
                f"P = ({uraikan_faktorial(total_items)}) / "
                f"({denominator_expansion})",
            ],
        ),
        (
            "Sederhanakan faktor yang sama",
            (
                f"Faktorial terbesar pada penyebut adalah {largest_count}! "
                f"(kelompok {largest_index + 1}). Faktor itu juga muncul pada "
                "pembilang, jadi dapat dicoret."
                if largest_count >= 1
                else "Semua faktorial penyebut bernilai 1, sehingga tidak ada "
                "faktor yang dicoret."
            ),
            [
                f"P = ({susun_faktor(numerator_factors)}) / "
                f"({denominator_expansion})",
            ],
        ),
        (
            "Hitung pembilang dan penyebut",
            "Hitung pembilang dan penyebut secara terpisah.",
            [
                "Pembilang:",
                *numerator_lines,
                f"{susun_faktor(numerator_factors)} = "
                f"{format_angka(numerator_value)}",
                "Penyebut:",
                *denominator_lines,
                f"{susun_faktor(denominator_factors)} = "
                f"{format_angka(denominator_value)}",
            ],
        ),
        (
            "Lakukan pembagian",
            f"Bagi pembilang dengan penyebut: {format_angka(numerator_value)} "
            f"/ {format_angka(denominator_value)}.",
            [
                f"P = {format_angka(numerator_value)} / "
                f"{format_angka(denominator_value)}",
                f"P = {format_angka(result)}",
            ],
        ),
        (
            "Hasil akhir",
            f"Terdapat {format_angka(result)} susunan berbeda dari "
            f"{total_items} unsur dengan kelompok identik "
            f"{', '.join(map(str, group_counts))} (unsur identik tidak dibedakan).",
            [],
        ),
    ]
    return result, "P", steps


def buat_langkah_kombinasi_berulang(
    n: int, r: int
) -> tuple[int, str, list[Step]]:
    transformed_n = n + r - 1
    result = comb(transformed_n, r)
    label = f"C_ulang({n},{r})"
    _, _, standard_steps = buat_langkah_kombinasi(transformed_n, r)
    transformed_steps = standard_steps[:-1]
    transformed_steps[0] = (
        "Ubah ke bentuk faktorial",
        f"Kombinasi C({transformed_n},{r}) ditulis dengan faktorial sebagai "
        f"{transformed_n}! dibagi {r}! dan ({transformed_n} - {r})!.",
        transformed_steps[0][2],
    )
    transformed_steps[1] = (
        "Substitusi ke bentuk faktorial",
        f"Pakai {transformed_n} sebagai pengganti n. Bagian dalam kurung: "
        f"{transformed_n} - {r} = {n - 1} (sama dengan n - 1).",
        transformed_steps[1][2],
    )
    steps: list[Step] = [
        (
            "Rumus umum",
            "n adalah banyak jenis elemen dan r adalah banyak elemen yang "
            "dipilih. Elemen boleh dipilih berulang dan urutan tidak "
            "diperhitungkan. Nilai r boleh lebih besar dari n.",
            [
                "C_ulang(n,r) = C(n + r - 1, r) "
                "= (n + r - 1)! / (r! (n - 1)!)"
            ],
        ),
        (
            "Substitusi nilai input",
            f"Ganti n dengan {n} dan r dengan {r}, lalu hitung "
            f"n + r - 1 = {n} + {r} - 1 = {transformed_n}.",
            [
                f"{label} = C({n} + {r} - 1, {r})",
                f"{label} = C({transformed_n}, {r})",
            ],
        ),
        *transformed_steps,
        (
            "Hasil akhir",
            f"Terdapat {format_angka(result)} cara memilih {r} elemen dari "
            f"{n} jenis elemen jika elemen yang sama boleh dipilih berulang "
            "kali dan urutan tidak diperhitungkan.",
            [],
        ),
    ]
    return result, label, steps


def tampilkan_hasil(
    method_name: str,
    formula: str,
    result: int,
    steps: list[Step],
    *,
    conclusion: str,
    daftar: Iterable[str] | None = None,
    jumlah_hasil: int = 0,
) -> None:
    print(f"\nProses Penghitungan {method_name}")
    print(f"Rumus metode: {formula}")
    for index, (title, description, math_lines) in enumerate(steps, 1):
        print(f"\nLangkah {index}: {title}")
        print(description)
        for line in math_lines:
            print(f"  {line}")
    print(f"\n{formula} = {format_angka(result)}")
    print(conclusion)
    if daftar is not None:
        tampilkan_daftar("Daftar hasil", daftar, jumlah_hasil)


def jalankan_permutasi_standar() -> None:
    n, r, unsur = baca_input_standar(
        defaults=(5, 3),
        require_r_at_most_n=True,
    )
    result, label, steps = buat_langkah_permutasi(n, r)
    tampilkan_hasil(
        "Permutasi Standar",
        label,
        result,
        steps,
        conclusion="Urutan diperhitungkan dan elemen tidak diulang.",
        daftar=hasil_berlabel(permutations(unsur, r)),
        jumlah_hasil=result,
    )


def jalankan_permutasi_berulang() -> None:
    n, r, unsur = baca_input_standar(
        defaults=(3, 2),
        require_r_at_most_n=False,
    )
    result, label, steps = buat_langkah_permutasi_berulang(n, r)
    tampilkan_hasil(
        "Permutasi Berulang",
        label,
        result,
        steps,
        conclusion="Urutan diperhitungkan dan elemen boleh diulang.",
        daftar=hasil_berlabel(product(unsur, repeat=r)),
        jumlah_hasil=result,
    )


def jalankan_unsur_identik() -> None:
    while True:
        group_count = baca_bilangan_bulat(
            "Jumlah kelompok unsur identik [2]: ",
            minimum=1,
            default=2,
        )
        group_counts = [
            baca_bilangan_bulat(f"Jumlah unsur pada kelompok {index} [2]: ", default=2)
            for index in range(1, group_count + 1)
        ]
        total_items = sum(group_counts)
        if total_items > MAX_INPUT:
            print(f"Total unsur ({total_items}) melebihi batas {MAX_INPUT}.")
            continue
        if group_count > total_items:
            print(
                f"Banyak kelompok ({group_count}) tidak boleh melebihi jumlah "
                f"seluruh unsur ({total_items})."
            )
            continue
        if baca_pilihan_ya_tidak(
            f"Hitung n otomatis dari total kelompok ({total_items})? [y]: ",
            default=True,
        ):
            break
        while True:
            n = baca_bilangan_bulat("Masukkan total n: ")
            if n == total_items:
                break
            print(
                f"Jumlah seluruh kelompok ({total_items}) harus sama dengan n ({n})."
            )
        break

    result, label, steps = buat_langkah_unsur_identik(group_counts)
    tampilkan_hasil(
        "Permutasi dengan Unsur Identik",
        label,
        result,
        steps,
        conclusion="Unsur dalam kelompok yang sama dianggap identik.",
    )


def jalankan_permutasi_melingkar() -> None:
    n = baca_bilangan_bulat("Masukkan n [4]: ", minimum=1, default=4)
    result, label, steps = buat_langkah_permutasi_melingkar(n)
    tampilkan_hasil(
        "Permutasi Melingkar",
        label,
        result,
        steps,
        conclusion="Susunan yang hanya berbeda karena rotasi dianggap sama.",
    )


def jalankan_kombinasi_standar() -> None:
    n, r, unsur = baca_input_standar(
        defaults=(5, 3),
        require_r_at_most_n=True,
    )
    result, label, steps = buat_langkah_kombinasi(n, r)
    tampilkan_hasil(
        "Kombinasi Standar",
        label,
        result,
        steps,
        conclusion="Urutan tidak diperhitungkan dan elemen tidak diulang.",
        daftar=hasil_berlabel(combinations(unsur, r)),
        jumlah_hasil=result,
    )


def jalankan_kombinasi_berulang() -> None:
    n, r, unsur = baca_input_standar(
        defaults=(3, 2),
        minimum_n=1,
        require_r_at_most_n=False,
    )
    result, label, steps = buat_langkah_kombinasi_berulang(n, r)
    tampilkan_hasil(
        "Kombinasi Berulang",
        label,
        result,
        steps,
        conclusion="Urutan tidak diperhitungkan dan elemen boleh diulang.",
        daftar=hasil_berlabel(combinations_with_replacement(unsur, r)),
        jumlah_hasil=result,
    )


PERMUTATION_METHODS = {
    "1": ("Permutasi Standar", jalankan_permutasi_standar),
    "2": ("Permutasi Berulang", jalankan_permutasi_berulang),
    "3": ("Unsur Identik", jalankan_unsur_identik),
    "4": ("Permutasi Melingkar", jalankan_permutasi_melingkar),
}

COMBINATION_METHODS = {
    "1": ("Kombinasi Standar", jalankan_kombinasi_standar),
    "2": ("Kombinasi Berulang", jalankan_kombinasi_berulang),
}


def tampilkan_rumus() -> None:
    print("\n=== RUMUS PERMUTASI & KOMBINASI ===")
    references = [
        (
            "Permutasi Standar",
            "P(n,r) = n! / (n - r)!",
            "Urutan diperhitungkan, elemen tidak diulang, 0 <= r <= n.",
        ),
        (
            "Permutasi dengan Pengulangan",
            "P_ulang(n,r) = n^r",
            "Urutan diperhitungkan dan elemen boleh diulang; r boleh lebih besar dari n.",
        ),
        (
            "Permutasi dengan Unsur Identik",
            "P = n! / (n1! x n2! x ... x nk!)",
            "Unsur pada kelompok yang sama identik; n = n1 + n2 + ... + nk.",
        ),
        (
            "Permutasi Melingkar",
            "P_melingkar(n) = (n - 1)!",
            "Susunan yang hanya berbeda karena rotasi dianggap sama; n minimal 1.",
        ),
        (
            "Kombinasi Standar",
            "C(n,r) = n! / (r! (n - r)!)",
            "Urutan tidak diperhitungkan dan elemen tidak diulang.",
        ),
        (
            "Kombinasi dengan Pengulangan",
            "C_ulang(n,r) = C(n + r - 1, r)",
            "Urutan tidak diperhitungkan, elemen boleh diulang, dan n minimal 1.",
        ),
    ]
    for title, formula, description in references:
        print(f"\n{title}")
        print(f"  {formula}")
        print(f"  {description}")
    print("\nPengertian Faktorial")
    print("  n! = n x (n - 1) x ... x 2 x 1")
    print("  0! = 1")
    print("  Contoh: 4! = 4 x 3 x 2 x 1 = 24")


def pilih_metode(
    title: str, methods: dict[str, tuple[str, MethodAction]]
) -> MethodAction | None:
    print(f"\n=== {title.upper()} ===")
    for key, (name, _) in methods.items():
        print(f"{key}. {name}")
    print("0. Kembali")
    choice = input("Pilih metode: ").strip()
    if choice == "0":
        return None
    selected = methods.get(choice)
    if selected is None:
        print("Pilihan metode tidak valid.")
        return None
    return selected[1]


def program_utama() -> None:
    while True:
        print("\n=== PERMUTASI & KOMBINASI ===")
        print("1. Permutasi")
        print("2. Kombinasi")
        print("3. Rumus")
        print("0. Keluar")
        choice = input("Pilih menu: ").strip()
        if choice == "0":
            print("Sampai jumpa!")
            return
        if choice == "3":
            tampilkan_rumus()
            continue
        if choice == "1":
            action = pilih_metode("Metode Permutasi", PERMUTATION_METHODS)
        elif choice == "2":
            action = pilih_metode("Metode Kombinasi", COMBINATION_METHODS)
        else:
            print("Pilihan tidak valid. Pilih menu 0 sampai 3.")
            continue
        if action is not None:
            try:
                action()
            except ValueError as error:
                print(f"Input tidak valid: {error}")


if __name__ == "__main__":
    program_utama()
