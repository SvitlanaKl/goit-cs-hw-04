import os
import threading
import time

def search_in_files(file_list, keywords, result_dict, lock):
    for file_path in file_list:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                for word in keywords:
                    if word in content:
                        with lock:
                            if word not in result_dict:
                                result_dict[word] = []
                            result_dict[word].append(file_path)
        except Exception as e:
            print(f"Помилка при обробці файлу {file_path}: {e}")

def threaded_search(files, keywords):
    num_threads = min(4, len(files))  # Кількість потоків не більше кількості файлів
    threads = []
    result_dict = {}
    lock = threading.Lock()

    # Розподіл файлів між потоками
    files_per_thread = len(files) // num_threads
    for i in range(num_threads):
        start_index = i * files_per_thread
        end_index = (i + 1) * files_per_thread if i != num_threads - 1 else len(files)
        thread_files = files[start_index:end_index]
        t = threading.Thread(target=search_in_files, args=(thread_files, keywords, result_dict, lock))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return result_dict

if __name__ == "__main__":
    import glob

    # Список файлів для обробки
    files = glob.glob('path/to/text/files/*.txt')
    keywords = ['слово1', 'слово2', 'слово3']

    start_time = time.time()
    results = threaded_search(files, keywords)
    end_time = time.time()

    print("Результати багатопотокового пошуку:")
    for word, file_list in results.items():
        print(f"{word}: {file_list}")

    print(f"Час виконання: {end_time - start_time:.2f} секунд")
