import uml_interpreter.model.base_classes as bc
import uml_interpreter.model.sequence_diagram as sd


class ClassDiagram(bc.StructuralDiagram):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.elements: list[ClassDiagramElement] = []


class ClassDiagramElement(sd.SequenceActor):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.relations_to: list[ClassRelationship] = []
        self.relations_from: list[ClassRelationship] = []
        self.methods: list[ClassDiagramMethod] = []


class ClassDiagramClass(ClassDiagramElement):
    def __init__(self, name: str) -> None:
        super().__init__(name)


class ClassDiagramInterface(ClassDiagramElement):
    def __init__(self, name: str) -> None:
        super().__init__(name)


class ClassRelationship:
    def __init__(
        self, source: ClassDiagramElement, target: ClassDiagramElement
    ) -> None:
        self.source = source
        source.relations_from.append(self)
        self.target = target
        target.relations_to.append(self)


class ClassDiagramMethod:
    def __init__(self, element: ClassDiagramElement, name: str) -> None:
        self.assigned_element = element
        element.methods.append(self)
        self.name = name
