def generate_plantuml(classes, relationships, direction="LR"):
    """
    Генерирует PlantUML код для диаграммы классов.
    
    :param classes: Список словарей с классами:
        [{'name': 'ClassName', 
          'attributes': ['+attr1: Type', '-attr2: Type'], 
          'methods': ['+method1(): ReturnType']}]
    :param relationships: Список словарей с отношениями:
        [{'from': 'ClassA', 'to': 'ClassB', 'type': 'inheritance'}, 
         {'from': 'ClassC', 'to': 'ClassD', 'type': 'association'}]
    :param direction: Направление рисования (LR, RL, TB, BT)
    :return: Строка с PlantUML кодом
    """
    plantuml = ["@startuml"]
    plantuml.append(f"left to right direction {direction}")
    plantuml.append("\n")

    # Добавляем классы
    for cls in classes:
        plantuml.append(f"class {cls['name']} {{")
        for attr in cls.get('attributes', []):
            plantuml.append(f"  {attr}")
        if cls.get('attributes') and cls.get('methods'):
            plantuml.append("  ..")
        for method in cls.get('methods', []):
            plantuml.append(f"  {method}")
        plantuml.append("}\n")

    # Добавляем отношения
    for rel in relationships:
        from_cls = rel['from']
        to_cls = rel['to']
        rel_type = rel['type'].lower()
        
        if rel_type == "inheritance":
            plantuml.append(f"{from_cls} <|-- {to_cls}")
        elif rel_type == "composition":
            plantuml.append(f"{from_cls} *-- {to_cls}")
        elif rel_type == "aggregation":
            plantuml.append(f"{from_cls} o-- {to_cls}")
        elif rel_type == "association":
            plantuml.append(f"{from_cls} --> {to_cls}")
        elif rel_type == "dependency":
            plantuml.append(f"{from_cls} ..> {to_cls}")
        elif rel_type == "realization":
            plantuml.append(f"{from_cls} ..|> {to_cls}")
        else:
            plantuml.append(f"{from_cls} -- {to_cls} : {rel_type}")

    plantuml.append("\n@enduml")
    return "\n".join(plantuml)