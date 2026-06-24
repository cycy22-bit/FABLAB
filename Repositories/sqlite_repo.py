import sqlite3
from datetime import date

from Models import MaterielDTO, EmpruntDTO
from Services.protocols import IMaterielRepository, IEmpruntRepository


class SQLiteMaterielRepository(IMaterielRepository):

    def __init__(self, database_path: str):
        self.database_path = database_path

    def get_connection(self):
        return sqlite3.connect(self.database_path)
    def get_all(self) -> list[MaterielDTO]:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id_materiel, nom_materiel, categorie, quantite_stock, stock_minimum
        FROM materiels
        """)

        rows = cursor.fetchall()
        conn.close()

        return [
            MaterielDTO(
                id_materiel=row[0],
                nom_materiel=row[1],
                categorie=row[2],
                quantite_stock=row[3],
                stock_minimum=row[4]
            )
            for row in rows
        ]
    def save(self, materiel: MaterielDTO) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO materiels (
            nom_materiel,
            categorie,
            quantite_stock,
            stock_minimum
        )
        VALUES (?, ?, ?, ?)
        """, (
            materiel.nom_materiel,
            materiel.categorie,
            materiel.quantite_stock,
            materiel.stock_minimum
        ))

        conn.commit()
        conn.close()

        return True
    
    def delete(self, materiel_id: int) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM materiels
        WHERE id_materiel = ?
        """, (materiel_id,))

        conn.commit()
        conn.close()

        return True
    def update_stock(self, materiel_id: int, nouvelle_quantite: int) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE materiels
        SET quantite_stock = ?
        WHERE id_materiel = ?
        """, (nouvelle_quantite, materiel_id))

        conn.commit()
        conn.close()

        return True
    def get_by_id(self, materiel_id: int) -> MaterielDTO | None:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id_materiel,
               nom_materiel,
               categorie,
               quantite_stock,
               stock_minimum
        FROM materiels
        WHERE id_materiel = ?
        """, (materiel_id,))

        row = cursor.fetchone()

        conn.close()

        if row is None:
            return None

        return MaterielDTO(
            id_materiel=row[0],
            nom_materiel=row[1],
            categorie=row[2],
            quantite_stock=row[3],
            stock_minimum=row[4]
        )
    
class SQLiteEmpruntRepository(IEmpruntRepository):

    def __init__(self, database_path: str):
        self.database_path = database_path

    def get_connection(self):
        return sqlite3.connect(self.database_path)

    def get_all(self) -> list[EmpruntDTO]:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id_emprunt, id_etudiant, id_materiel, quantite_empruntee,
               date_emprunt, date_retour_prevue, date_retour_effective,
               statut_emprunt, etat_retour
        FROM emprunts
        """)

        rows = cursor.fetchall()
        conn.close()

        return [
            EmpruntDTO(
                id_emprunt=row[0],
                id_etudiant=row[1],
                id_materiel=row[2],
                quantite_empruntee=row[3],
                date_emprunt=date.fromisoformat(row[4]),
                date_retour_prevue=date.fromisoformat(row[5]),
                date_retour_effective=date.fromisoformat(row[6]) if row[6] else None,
                statut_emprunt=row[7],
                etat_retour=row[8]
            )
            for row in rows
        ]

    def save(self, emprunt: EmpruntDTO) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO emprunts (
            id_etudiant,
            id_materiel,
            quantite_empruntee,
            date_emprunt,
            date_retour_prevue,
            date_retour_effective,
            statut_emprunt,
            etat_retour
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            emprunt.id_etudiant,
            emprunt.id_materiel,
            emprunt.quantite_empruntee,
            emprunt.date_emprunt.isoformat(),
            emprunt.date_retour_prevue.isoformat(),
            emprunt.date_retour_effective.isoformat() if emprunt.date_retour_effective else None,
            emprunt.statut_emprunt,
            emprunt.etat_retour
        ))

        conn.commit()
        conn.close()

        return True

    def update_status(self, emprunt_id: int, statut: str) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE emprunts
        SET statut_emprunt = ?
        WHERE id_emprunt = ?
        """, (statut, emprunt_id))

        conn.commit()
        conn.close()

        return True

    def delete(self, emprunt_id: int) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM emprunts
        WHERE id_emprunt = ?
        """, (emprunt_id,))

        conn.commit()
        conn.close()

        return True