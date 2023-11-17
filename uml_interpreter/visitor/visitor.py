from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uml_interpreter.model.base_classes import UMLDiagram, UMLModel
    from uml_interpreter.model.class_diagram import (ClassDiagram,
                                                     ClassDiagramAttribute,
                                                     ClassDiagramClass,
                                                     ClassDiagramElement,
                                                     ClassDiagramInterface,
                                                     ClassDiagramMethod,
                                                     ClassRelationship)


class ModelVisitor(ABC):
    @abstractmethod
    def visit_model(self, model: UMLModel):
        pass

    @abstractmethod
    def visit_diagram(self, diag: UMLDiagram):
        pass

    @abstractmethod
    def visit_class_diagram(self, diag: ClassDiagram):
        pass

    @abstractmethod
    def visit_class_diagram_element(self, elem: ClassDiagramElement):
        pass

    @abstractmethod
    def visit_class_diagram_class(self, elem: ClassDiagramClass):
        pass

    @abstractmethod
    def visit_class_diagram_interface(self, elem: ClassDiagramInterface):
        pass

    @abstractmethod
    def visit_class_relationship(self, diag: ClassRelationship):
        pass

    @abstractmethod
    def visit_class_diagram_attribute(self, diag: ClassDiagramAttribute):
        pass

    @abstractmethod
    def visit_diagram_method(self, diag: ClassDiagramMethod):
        pass


class ModelPrinter(ModelVisitor):
    def __init__(self, indent: int = 0, indent_inc: int = 2) -> None:
        self._indent = indent
        self._indent_inc = indent_inc

    def visit_model(self, model: UMLModel) -> None:
        self.print("Model:")

        self.incr_ident()
        for diagram in model.diagrams:
            diagram.accept(self)
        self.decr_ident()

    def visit_diagram(self, diagram: UMLDiagram) -> None:
        self.print(f'UML Diagram: "{diagram.name}"')

    def visit_class_diagram(self, diagram: ClassDiagram) -> None:
        self.print(f'Class Diagram: "{diagram.name}"')

        self.incr_ident()
        for elem in diagram.elements:
            elem.accept(self)
        self.decr_ident()

    def visit_class_diagram_element(self, elem: ClassDiagramElement):
        self.print(f'Element: "{elem.name}"')

        self.incr_ident()
        self.visit_class_diagram_element_data(elem)
        self.decr_ident()

    def visit_class_diagram_class(self, elem: ClassDiagramClass):
        self.print(f'Class: "{elem.name}"')

        self.incr_ident()
        self.visit_class_diagram_element_data(elem)
        self.decr_ident()

    def visit_class_diagram_interface(self, elem: ClassDiagramInterface):
        self.print(f'Interface: "{elem.name}"')

        self.incr_ident()
        self.visit_class_diagram_element_data(elem)
        self.decr_ident()

    def visit_class_diagram_element_data(self, elem: ClassDiagramElement):
        if (len(elem.relations_from) > 0):
            self.print("Relationships (source):")
            self.incr_ident()
            for rel in elem.relations_from:
                rel.accept(self)
            self.decr_ident()

        if (len(elem.relations_to) > 0):
            self.print("Relationships (target):")
            self.incr_ident()
            for rel in elem.relations_to:
                rel.accept(self)
            self.decr_ident()

        if (len(elem.attributes) > 0):
            self.print("Attributes:")
            self.incr_ident()
            for rel in elem.attributes:
                rel.accept(self)
            self.decr_ident()

        if (len(elem.methods) > 0):
            self.print("Methods:")
            self.incr_ident()
            for rel in elem.methods:
                rel.accept(self)
            self.decr_ident()

    def visit_class_relationship(self, rel: ClassRelationship):
        from uml_interpreter.model.class_diagram import ClassDiagramElement

        if isinstance(rel.source, ClassDiagramElement) and isinstance(rel.target, ClassDiagramElement):
            self.print(f"{rel.type} - {rel.source.name} -> {rel.target.name}")

    def visit_class_diagram_attribute(self, attr: ClassDiagramAttribute):
        self.print(f"{attr.name}: {attr.type}")

    def visit_diagram_method(self, meth: ClassDiagramMethod):
        self.print(f"{meth.name}: {[f'{attr.name}: {attr.type}' for attr in meth.attributes]} -> {meth.ret_type}")

    def incr_ident(self) -> None:
        self._indent = self._indent + self._indent_inc

    def decr_ident(self) -> None:
        self._indent = self._indent - self._indent_inc

    def print(self, mess: str) -> None:
        print('|' + '-' * self._indent + mess)
