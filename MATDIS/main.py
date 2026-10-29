"""Versi terminal dari suite permutasi dan kombinasi pada index.html."""

from collections import Counter
from itertools import combinations, combinations_with_replacement, permutations
from math import comb, factorial
from pathlib import Path
from typing import Iterable, Iterator, Sequence


LIST_CAP = 10_000
FIRST_PAGE_SIZE = 50
PAGE_SIZE = 500
MAX_N = 100

MODES = {
    "1": ("Permutasi Standar", "perm"),
    "2": ("Kombinasi Standar", "comb"),
    "3": ("Permutasi Unsur Sama (Multiset)", "repeats"),
    "4": ("Kombinasi Berulang & Permutasi Siklis", "rep_circ"),
    "5": ("Hubungan Permutasi dan Kombinasi", "relation"),
    "6": ("Visualizer Backtracking", "anim"),
}

PRESETS = {
    "1": ("P(3,2) [A, B, C]", "perm", 3, 2, ["A", "B", "C"]),
    "2": (
        "C(5,3) Nama",
        "comb",
        5,
        3,
        ["Ani", "Budi", "Cici", "Dedi", "Eka"],
    ),
    "3": (
        "Unsur Sama (BANANA)",
        "repeats",
        6,
        None,
        ["B", "A", "N", "A", "N", "A"],
    ),
    "4": (
        "Pengulangan & Siklis",
        "rep_circ",
        4,
        3,
        ["A", "B", "C", "D"],
    ),
    "5": ("Hubungan P vs C", "relation", 4, 2, ["A", "B", "C", "D"]),
    "6": ("Animasi Visual", "anim", 3, 2, ["A", "B", "C"]),
}


def format_number(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def permutation_count(n: int, r: int) -> int:
    return factorial(n) // factorial(n - r)


def combination_count(n: int, r: int) -> int:
    return comb(n, r)


def default_items(n: int) -> list[str]:
    if n <= 26:
        return [chr(ord("A") + index) for index in range(n)]
    return [str(index + 1) for index in range(n)]


def read_nonnegative_int(prompt: str, maximum: int | None = None) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Masukkan bilangan bulat.")
            continue
        if value < 0:
            print("Nilai tidak boleh negatif.")
            continue
        if maximum is not None and value > maximum:
            print(f"Nilai maksimal adalah {maximum}.")
            continue
        return value


def parse_items(raw: str, allow_duplicates: bool) -> list[str] | None:
    if not raw.strip():
        return None
    items = [item.strip() for item in raw.split(",") if item.strip()]
    if not items:
        raise ValueError("Daftar item tidak valid.")
    if not allow_duplicates and len(set(items)) != len(items):
        duplicates = sorted(item for item, count in Counter(items).items() if count > 1)
        raise ValueError(
            "Item harus unik pada moda ini. Item berulang: "
            + ", ".join(duplicates)
            + '. Gunakan "Permutasi Unsur Sama" jika item memang berulang.'
        )
    if len(items) > MAX_N:
        raise ValueError(f"Jumlah item maksimal adalah {MAX_N}.")
    return items


def get_inputs(
    mode: str, preset: tuple[int, int | None, list[str]] | None = None
) -> tuple[int, int | None, list[str]]:
    allow_duplicates = mode in {"repeats", "rep_circ"}
    if preset is None:
        n = read_nonnegative_int(f"Masukkan n (maksimal {MAX_N}): ", MAX_N)
        while True:
            try:
                items = parse_items(
                    input(
                        "Masukkan item dipisahkan koma "
                        "(kosong = gunakan A, B, C, ...): "
                    ),
                    allow_duplicates,
                )
                break
            except ValueError as error:
                print(f"Input item tidak valid: {error}")
        if items is not None:
            n = len(items)
            print(f"n disesuaikan menjadi {n} mengikuti jumlah item.")
        else:
            items = default_items(n)
    else:
        n, _, items = preset

    if mode == "repeats":
        return n, None, items

    if preset is None:
        while True:
            r = read_nonnegative_int("Masukkan r: ")
            if mode not in {"perm", "comb", "relation", "anim"} or r <= n:
                break
            print(f"Nilai r ({r}) tidak boleh lebih besar dari n ({n}).")
    else:
        r = preset[1]
        assert r is not None

    if mode in {"perm", "comb", "relation", "anim"} and r > n:
        raise ValueError(f"Nilai r ({r}) tidak boleh lebih besar dari n ({n}).")
    return n, r, items


def bounded_results(results: Iterable[Sequence[str]]) -> Iterator[str]:
    for index, result in enumerate(results):
        if index >= LIST_CAP:
            return
        yield " ".join(result) if result else "(kosong)"


def show_results(
    title: str,
    results: Iterable[str],
    total: int,
    mode_name: str,
) -> list[str]:
    iterator = iter(results)
    shown: list[str] = []
    limit = min(total, LIST_CAP)
    batch_size = min(FIRST_PAGE_SIZE, limit)

    while len(shown) < limit:
        count = min(batch_size, limit - len(shown))
        for _ in range(count):
            try:
                shown.append(next(iterator))
            except StopIteration:
                break
        print(f"\n{title} - menampilkan {len(shown)} dari {format_number(total)}:")
        start = max(0, len(shown) - count)
        for index in range(start, len(shown)):
            print(f"{index + 1:>5}. {shown[index]}")
        if len(shown) >= limit or len(shown) == total:
            break
        action = input(
            "\nEnter: 500 berikutnya | a: tampilkan semua | "
            "s: lewati daftar: "
        ).strip().lower()
        if action == "s":
            break
        batch_size = limit - len(shown) if action == "a" else PAGE_SIZE

    if total > LIST_CAP:
        print(f"Daftar dibatasi hingga {format_number(LIST_CAP)} hasil pertama.")
    if not shown:
        print(f"\n{title}: tidak ada hasil.")

    if shown and input("\nSimpan hasil yang ditampilkan ke file .txt? (y/n): ").strip().lower() == "y":
        path = Path(__file__).with_name(f"hasil_{mode_name}.txt")
        with path.open("w", encoding="utf-8") as output:
            output.write(f"=== HASIL PERHITUNGAN {mode_name.upper()} ===\n")
            output.write(f"Total kemungkinan: {format_number(total)}\n")
            output.write(f"Jumlah yang disimpan: {len(shown)}\n\nDaftar:\n")
            output.writelines(
                f"{index}. {result}\n" for index, result in enumerate(shown, 1)
            )
        print(f"Hasil disimpan di: {path}")
    return shown


def unique_permutations(items: Sequence[str]) -> Iterator[tuple[str, ...]]:
    counts = Counter(items)
    keys = sorted(counts)
    current: list[str] = []

    def generate() -> Iterator[tuple[str, ...]]:
        if len(current) == len(items):
            yield tuple(current)
            return
        for item in keys:
            if counts[item] == 0:
                continue
            counts[item] -= 1
            current.append(item)
            yield from generate()
            current.pop()
            counts[item] += 1

    yield from generate()


def print_permutation(n: int, r: int, items: list[str]) -> None:
    total = permutation_count(n, r)
    print(f"\nModa: Permutasi Standar")
    print(f"n = {n}, r = {r}")
    print(f"Langkah 1: P({n},{r}) = {n}! / ({n} - {r})!")
    print(f"Langkah 2: P({n},{r}) = {n}! / {n-r}! = {format_number(total)}")
    print("Urutan diperhitungkan.")
    show_results(
        "Daftar Permutasi",
        bounded_results(permutations(items, r)),
        total,
        "perm",
    )


def print_combination(n: int, r: int, items: list[str]) -> None:
    total = combination_count(n, r)
    print(f"\nModa: Kombinasi Standar")
    print(f"n = {n}, r = {r}")
    print(f"Langkah 1: C({n},{r}) = {n}! / ({r}! x ({n} - {r})!)")
    print(f"Langkah 2: C({n},{r}) = {format_number(total)}")
    print("Urutan tidak diperhitungkan.")
    show_results(
        "Daftar Kombinasi",
        bounded_results(combinations(items, r)),
        total,
        "comb",
    )


def print_multiset(items: list[str]) -> None:
    counts = Counter(items)
    denominator = 1
    for count in counts.values():
        denominator *= factorial(count)
    total = factorial(len(items)) // denominator
    frequencies = ", ".join(
        f"{item}: {count}" for item, count in sorted(counts.items())
    )
    denominator_formula = " x ".join(
        f"{count}!" for count in counts.values()
    ) or "1"
    print("\nModa: Permutasi Unsur Sama (Multiset)")
    print(f"n = {len(items)}")
    print(f"Frekuensi elemen: {frequencies}")
    print(f"P = {len(items)}! / ({denominator_formula})")
    print(f"Total susunan unik = {format_number(total)}")
    show_results(
        "Daftar Susunan Unik",
        bounded_results(unique_permutations(items)),
        total,
        "repeats",
    )


def print_repetition_and_circular(n: int, r: int, items: list[str]) -> None:
    repeated_total = comb(n + r - 1, r) if n else int(r == 0)
    circular_total = factorial(n - 1) if n else 0
    print("\nModa: Kombinasi Berulang & Permutasi Siklis")
    print(f"n = {n}, r = {r}")
    print(
        f"Kombinasi berulang: C'({n},{r}) = "
        f"C({n} + {r} - 1,{r}) = {format_number(repeated_total)}"
    )
    print(
        f"Permutasi siklis: P_siklis({n}) = ({n} - 1)! "
        f"= {format_number(circular_total)}"
    )
    show_results(
        "Daftar Kombinasi dengan Pengulangan",
        bounded_results(combinations_with_replacement(items, r)),
        repeated_total,
        "rep_circ",
    )


def print_relation(n: int, r: int, items: list[str]) -> None:
    c_value = combination_count(n, r)
    p_value = permutation_count(n, r)
    r_factorial = factorial(r)
    print("\nModa: Hubungan Permutasi dan Kombinasi")
    print(f"P({n},{r}) = C({n},{r}) x {r}!")
    print(
        f"{format_number(p_value)} = {format_number(c_value)} x "
        f"{format_number(r_factorial)}"
    )
    print("Pengelompokan permutasi berdasarkan kombinasinya:")

    def groups() -> Iterator[str]:
        per_group_limit = r_factorial if p_value <= LIST_CAP else 50
        for index, selected in enumerate(combinations(items, r), 1):
            group_permutations: list[str] = []
            for permutation_index, permutation in enumerate(permutations(selected)):
                if permutation_index == per_group_limit:
                    break
                group_permutations.append(" ".join(permutation))
            yield (
                f"Kombinasi #{index}: {{ {', '.join(selected)} }} -> "
                + " | ".join(group_permutations)
            )

    group_total = min(c_value, LIST_CAP)
    show_results(
        "Kelompok Kombinasi",
        groups(),
        group_total,
        "relation",
    )
    if p_value > LIST_CAP:
        print(
            "Catatan: hasil dibatasi; setiap kelompok menampilkan maksimal "
            "50 susunan dan daftar maksimal 10.000 kelompok."
        )


def backtracking_steps(
    current: list[str], available: list[str], r: int
) -> Iterator[tuple[str, list[str]]]:
    yield ("PILIH", current.copy())
    if len(current) == r:
        yield ("DITEMUKAN", current.copy())
        return
    for index, item in enumerate(available):
        current.append(item)
        yield from backtracking_steps(
            current, available[:index] + available[index + 1 :], r
        )
        current.pop()
        yield ("KEMBALI", current.copy())


def print_animation(n: int, r: int, items: list[str]) -> None:
    print("\nModa: Visualizer Backtracking (Permutasi)")
    if n > 5 or r > 4:
        print("Visualisasi memerlukan n <= 5 dan r <= 4.")
        return
    steps = list(backtracking_steps([], items[:n], r))
    step_by_step = input("Jalankan langkah satu per satu? (y/n): ").strip().lower() == "y"
    for index, (action, path) in enumerate(steps, 1):
        path_text = ", ".join(path) if path else "Root"
        message = {
            "PILIH": "Pilih/kunjungi",
            "DITEMUKAN": "Susunan ditemukan",
            "KEMBALI": "Backtrack ke",
        }[action]
        print(f"[Langkah {index}/{len(steps)}] {message}: [{path_text}]")
        if step_by_step and index < len(steps):
            input("Tekan Enter untuk lanjut...")


def print_formulas() -> None:
    print("\nRumus Permutasi & Kombinasi")
    print("1. Permutasi standar:       P(n,r) = n! / (n-r)!")
    print("2. Kombinasi standar:       C(n,r) = n! / (r! (n-r)!)")
    print("3. Permutasi unsur sama:    P = n! / (n1! n2! ... nk!)")
    print("4. Kombinasi pengulangan:   C'(n,r) = C(n+r-1,r)")
    print("5. Permutasi siklis:        P_siklis = (n-1)!")


def run_mode(
    mode: str, preset: tuple[int, int | None, list[str]] | None = None
) -> None:
    n, r, items = get_inputs(mode, preset)
    if mode == "repeats":
        print_multiset(items)
        return
    assert r is not None
    if mode == "perm":
        print_permutation(n, r, items)
    elif mode == "comb":
        print_combination(n, r, items)
    elif mode == "rep_circ":
        print_repetition_and_circular(n, r, items)
    elif mode == "relation":
        print_relation(n, r, items)
    elif mode == "anim":
        print_animation(n, r, items)


def print_menu() -> None:
    print("\n=== PERMUTASI & KOMBINASI (TERMINAL) ===")
    for key, (title, _) in MODES.items():
        print(f"{key}. {title}")
    print("7. Rumus")
    print("8. Contoh cepat")
    print("0. Keluar")


def run_preset() -> None:
    print("\nContoh cepat:")
    for key, (title, _, _, _, _) in PRESETS.items():
        print(f"{key}. {title}")
    print("0. Kembali")
    choice = input("Pilih contoh: ").strip()
    if choice == "0":
        return
    preset = PRESETS.get(choice)
    if preset is None:
        print("Pilihan contoh tidak valid.")
        return
    title, mode, n, r, items = preset
    print(f"\nContoh: {title}")
    run_mode(mode, (n, r, items))


def main() -> None:
    while True:
        print_menu()
        choice = input("Pilih menu: ").strip()
        if choice == "0":
            print("Sampai jumpa!")
            return
        if choice == "7":
            print_formulas()
            continue
        if choice == "8":
            run_preset()
            continue
        selected_mode = MODES.get(choice)
        if selected_mode is None:
            print("Pilihan tidak valid. Pilih menu 0 sampai 8.")
            continue
        try:
            run_mode(selected_mode[1])
        except ValueError as error:
            print(f"Input tidak valid: {error}")


if __name__ == "__main__":
    main()