from collections import defaultdict


def main():
    owners = {}
    waiting = {}
    processes = set()

    try:
        with open("waitlog.txt", encoding="utf-8") as file:
            lines = file.readlines()
    except OSError as error:
        print(f"ОШИБКА: не удалось открыть waitlog.txt: {error}")
        return

    for line_number, line in enumerate(lines, start=1):
        parts = line.split()

        if not parts:
            continue

        if len(parts) != 3:
            print(f"Строка {line_number}: неверный формат, пропускаем")
            continue

        event, pid, resource = parts
        processes.add(pid)

        if event == "acquire":
            if resource in owners and owners[resource] != pid:
                print(
                    f"Строка {line_number}: ресурс {resource} "
                    "уже принадлежит другому процессу"
                )
                continue

            owners[resource] = pid

            if waiting.get(pid) == resource:
                del waiting[pid]

        elif event == "release":
            if owners.get(resource) == pid:
                del owners[resource]

            if waiting.get(pid) == resource:
                del waiting[pid]

        elif event == "wait":
            waiting[pid] = resource

        else:
            print(
                f"Строка {line_number}: неизвестное событие {event}, "
                "пропускаем"
            )

    graph = defaultdict(set)

    for pid, resource in waiting.items():
        owner = owners.get(resource)

        if owner is not None and owner != pid:
            graph[pid].add(owner)

    for pid in processes:
        graph[pid]

    print("Граф ожидания на конец журнала:")

    has_edges = False

    for pid in sorted(graph):
        for target in sorted(graph[pid]):
            print(f"  {pid} -> {target}")
            has_edges = True

    if not has_edges:
        print("  Рёбер нет")

    # Поиск всех вершин, входящих в циклы, методом Тарьяна.
    index = 0
    indices = {}
    lowlink = {}
    stack = []
    on_stack = set()
    cycle_members = set()

    def strongconnect(vertex):
        nonlocal index

        indices[vertex] = index
        lowlink[vertex] = index
        index += 1

        stack.append(vertex)
        on_stack.add(vertex)

        for neighbor in graph[vertex]:
            if neighbor not in indices:
                strongconnect(neighbor)
                lowlink[vertex] = min(
                    lowlink[vertex], lowlink[neighbor]
                )
            elif neighbor in on_stack:
                lowlink[vertex] = min(
                    lowlink[vertex], indices[neighbor]
                )

        if lowlink[vertex] == indices[vertex]:
            component = []

            while True:
                node = stack.pop()
                on_stack.remove(node)
                component.append(node)

                if node == vertex:
                    break

            if len(component) > 1:
                cycle_members.update(component)
            elif component[0] in graph[component[0]]:
                cycle_members.add(component[0])

    for pid in sorted(graph):
        if pid not in indices:
            strongconnect(pid)

    print("\nУчастники циклов:")

    if cycle_members:
        print("  " + ", ".join(sorted(cycle_members)))
    else:
        print("  Циклов нет")

    # Процессы, которые могут дойти до цикла по направлению ожидания.
    blocked_forever = set()

    for start in graph:
        visited = set()
        todo = [start]
        reaches_cycle = False

        while todo:
            current = todo.pop()

            if current in visited:
                continue

            visited.add(current)

            if current in cycle_members:
                reaches_cycle = True
                break

            todo.extend(graph[current] - visited)

        if reaches_cycle and start not in cycle_members:
            blocked_forever.add(start)

    print("\nЗаблокированы навсегда, но не входят в цикл:")

    if blocked_forever:
        print("  " + ", ".join(sorted(blocked_forever)))
    else:
        print("  Нет")


if __name__ == "__main__":
    main()
