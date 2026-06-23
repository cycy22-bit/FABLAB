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
    
class SQLiteEmpruntRepository(IEmpruntRepository):

    def __init__(self, database_path: str):
        self.database_path = database_path

    def get_connection(self):
        return sqlite3.connect(self.database_path)

    def get_all(self) -> list[EmpruntDTO]:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id_emprunt, id_etudiant, id_materiel, quantite,
               date_emprunt, date_retour_prevue, statut_emprunt
        FROM emprunts
        """)

        rows = cursor.fetchall()
        conn.close()

        return [
            EmpruntDTO(
                id_emprunt=row[0],
                id_etudiant=row[1],
                id_materiel=row[2],
                quantite=row[3],
                date_emprunt=date.fromisoformat(row[4]),
                date_retour_prevue=date.fromisoformat(row[5]),
                statut_emprunt=row[6]
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
            quantite,
            date_emprunt,
            date_retour_prevue,
            statut_emprunt
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            emprunt.id_etudiant,
            emprunt.id_materiel,
            emprunt.quantite,
            emprunt.date_emprunt.isoformat(),
            emprunt.date_retour_prevue.isoformat(),
            emprunt.statut_emprunt
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