import json
import sys


def is_safe(available, processes):
    work = available.copy()
    finished = set()

    while True:
        found = False

        for pid, data in processes.items():
            if pid in finished:
                continue

            allocation = data["allocation"]
            maximum = data["max"]
            need = [
                maximum[i] - allocation[i]
                for i in range(len(work))
            ]

            if all(need[i] <= work[i] for i in range(len(work))):
                work = [
                    work[i] + allocation[i]
                    for i in range(len(work))
                ]
                finished.add(pid)
                found = True

        if not found:
            break

    return len(finished) == len(processes)


def main():
    try:
        with open("system.json", encoding="utf-8") as file:
            system = json.load(file)

        resources = system["resources"]
        available = system["available"]
        processes = system["processes"]

        if len(available) != len(resources):
            raise ValueError("Размер available не совпадает с ресурсами")

        if any(not isinstance(x, int) or x < 0 for x in available):
            raise ValueError("available должен содержать неотрицательные целые числа")

        for pid, data in processes.items():
            allocation = data["allocation"]
            maximum = data["max"]

            if len(allocation) != len(resources) or len(maximum) != len(resources):
                raise ValueError(f"{pid}: неправильное количество ресурсов")

            if any(
                not isinstance(x, int) or x < 0
                for x in allocation + maximum
            ):
                raise ValueError(f"{pid}: ресурсы должны быть неотрицательными целыми")

            if any(allocation[i] > maximum[i] for i in range(len(resources))):
                raise ValueError(f"{pid}: allocation превышает max")

        with open("requests.txt", encoding="utf-8") as file:
            requests = file.readlines()

    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"ОШИБКА конфигурации: {error}")
        sys.exit(1)

    for line_number, line in enumerate(requests, start=1):
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        parts = line.split()

        if len(parts) != len(resources) + 1:
            print(f"Строка {line_number}: ОШИБКА — неверный формат запроса")
            continue

        pid = parts[0]

        try:
            request = [int(x) for x in parts[1:]]
        except ValueError:
            print(f"Строка {line_number}: ОШИБКА — ресурсы должны быть целыми числами")
            continue

        if any(x < 0 for x in request):
            print(f"{pid}: ОШИБКА — отрицательное количество ресурсов")
            continue

        if pid not in processes:
            print(f"{pid}: ОШИБКА — процесс не существует")
            continue

        data = processes[pid]
        allocation = data["allocation"]
        maximum = data["max"]

        need = [
            maximum[i] - allocation[i]
            for i in range(len(resources))
        ]

        if any(request[i] > need[i] for i in range(len(resources))):
            print(f"{pid}: ОТКАЗАТЬ — запрос превышает оставшуюся потребность")
            continue

        if any(request[i] > available[i] for i in range(len(resources))):
            print(f"{pid}: ОТКАЗАТЬ — недостаточно свободных ресурсов")
            continue

        old_available = available.copy()
        old_allocation = allocation.copy()

        available = [
            available[i] - request[i]
            for i in range(len(resources))
        ]

        data["allocation"] = [
            allocation[i] + request[i]
            for i in range(len(resources))
        ]

        if is_safe(available, processes):
            print(f"{pid}: ВЫДАТЬ — состояние системы безопасно")
        else:
            available = old_available
            data["allocation"] = old_allocation
            print(f"{pid}: ОТКАЗАТЬ — запрос создаёт небезопасное состояние, выполнен откат")


if __name__ == "__main__":
    main()
