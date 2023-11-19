from typing import Optional

import uml_interpreter.visitor.visitor as v


class UMLModel:
    def __init__(self, diagrams=None, filename=None) -> None:
        self.diagrams: list[UMLDiagram] = diagrams or []
        self.filename: Optional[str] = filename

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_model(self)

    def print(self, indent: int = 0, indent_inc: int = 2):
        self.accept(v.ModelPrinter(indent, indent_inc))


class UMLDiagram:
    def __init__(self, name: str | None = None) -> None:
        self.name: str = name or ""

    def accept(self, visitor: v.ModelVisitor):
        visitor.visit_diagram(self)


class StructuralDiagram(UMLDiagram):
    def __init__(self, name: str | None = None) -> None:
        super().__init__(name)


class BehavioralDiagram(UMLDiagram):
    def __init__(self, name: str | None = None) -> None:
        super().__init__(name)
