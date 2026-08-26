from app.repositories.database import get_connection


class ModelRepository:

    def save(self, model):
        connection = get_connection()
        cursor = connection.cursor()

        sql = """
        INSERT INTO models (name, year, brand_id)
        VALUES (%s, %s, %s)
        """

        values = (
            model.name,
            model.year,
            model.brand_id
        )

        cursor.execute(sql, values)
        connection.commit()

        model.id = cursor.lastrowid

        cursor.close()
        connection.close()

        return model

    def find_by_id(self, model_id):
        connection = get_connection()
        cursor = connection.cursor()

        sql = """
        SELECT id, name, year, brand_id
        FROM models
        WHERE id = %s
        """

        cursor.execute(sql, (model_id,))

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result

    def find_all(self):
        connection = get_connection()
        cursor = connection.cursor()

        sql = """
        SELECT id, name, year, brand_id
        FROM models
        """

        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        return results

    def find_by_brand_id(self, brand_id):
        connection = get_connection()
        cursor = connection.cursor()

        sql = """
        SELECT id, name, year, brand_id
        FROM models
        WHERE brand_id = %s
        """

        cursor.execute(sql, (brand_id,))

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        return results

    def update(self, model):
        connection = get_connection()
        cursor = connection.cursor()

        sql = """
        UPDATE models
        SET name = %s,
            year = %s,
            brand_id = %s
        WHERE id = %s
        """

        values = (
            model.name,
            model.year,
            model.brand_id,
            model.id
        )

        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()

    def delete(self, model_id):
        connection = get_connection()
        cursor = connection.cursor()

        sql = """
        DELETE FROM models
        WHERE id = %s
        """

        cursor.execute(sql, (model_id,))
        connection.commit()

        cursor.close()
        connection.close()