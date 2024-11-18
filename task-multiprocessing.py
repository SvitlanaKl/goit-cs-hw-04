import os
import multiprocessing
import time
from pathlib import Path

def search_in_files_process(file_list, keywords, queue):
    result = {}
    for file_path in file_list:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                for word in keywords:
                    if word in content:
                        if word not in result:
                            result[word] = []
                        result[word].append(str(file_path))
        except Exception as e:
            print(f"Помилка при обробці файлу {file_path}: {e}")
    queue.put(result)

def multiprocessing_search(files, keywords):
    num_processes = min(4, len(files))  # Кількість процесів не більше кількості файлів
    processes = []
    queue = multiprocessing.Queue()

    # Розподіл файлів між процесами
    files_per_process = len(files) // num_processes
    for i in range(num_processes):
        start_index = i * files_per_process
        end_index = (i + 1) * files_per_process if i != num_processes - 1 else len(files)
        process_files = files[start_index:end_index]
        p = multiprocessing.Process(target=search_in_files_process, args=(process_files, keywords, queue))
        processes.append(p)
        p.start()

    # Збирання результатів
    total_results = {}
    for _ in processes:
        partial_result = queue.get()
        for word, files in partial_result.items():
            if word not in total_results:
                total_results[word] = []
            total_results[word].extend(files)

    for p in processes:
        p.join()

    return total_results

if __name__ == "__main__":
    # Шлях до каталогу з файлами
    directory = Path(r"C:\Users\WORK\Desktop\GoIT\Repository\Computer_Systems\goit-cs-hw-04\text_files")

    # Список файлів для обробки
    files = list(directory.glob('*.txt'))
    keywords = ['черги', 'процес', 'канал']

    start_time = time.time()
    results = multiprocessing_search(files, keywords)
    end_time = time.time()

    print("Результати багатопроцесорного пошуку:")
    for word, file_list in results.items():
        print(f"{word}: {file_list}")

    print(f"Час виконання: {end_time - start_time:.2f} секунд")
