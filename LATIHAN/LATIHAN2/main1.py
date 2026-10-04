def merge_sort(arr, is_ascending=True):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], is_ascending)
    right = merge_sort(arr[mid:], is_ascending)

    return merge(left, right, is_ascending)


def merge(left, right, is_ascending):
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if is_ascending:
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        else:
            if left[i] >= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


print("======== Program Merge Sort ========")

while True:
    try:
        jumlah_data = int(input("Masukkan jumlah data: "))
        if jumlah_data <= 0:
            print("Jumlah data harus lebih dari 0!\n")
        else:
            break
    except ValueError:
        print("Input tidak valid! Harap masukkan angka bulat.\n")

data_list = []
print("\nMasukkan data satu per satu:")

for i in range(jumlah_data):
    while True:
        try:
            angka = int(input(f"Masukkan data ke-{i + 1}: "))
            data_list.append(angka)
            break
        except ValueError:
            print("Input tidak valid! Harap masukkan angka bulat.\n")

print("\nPilih metode pengurutan:")
print("1. Ascending")
print("2. Descending")

while True:
    pilihan = input("Masukkan pilihan (1/2): ")

    if pilihan == '1':
        pilih_asc = True
        break
    elif pilihan == '2':
        pilih_asc = False
        break
    else:
        print("Pilihan tidak valid! Ketik 1 atau 2.\n")

print("\nData sebelum diurutkan:", data_list)
hasil_urut = merge_sort(data_list, is_ascending=pilih_asc)
print("Data setelah diurutkan:", hasil_urut)

