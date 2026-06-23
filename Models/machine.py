from dataclasses import dataclass


@dataclass
class MachineDTO:
    id_machine: int | None
    nom_machine: str
    type_machine: str
    statut_machine: str
    emplacement: str