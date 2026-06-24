from dataclasses import dataclass


@dataclass
class MachineDTO:
    id_machine: int | None
    nom_machine: str
    type_machine: str
    description: str
    caracteristique_tech: str
    statut: str
    emplacement: str