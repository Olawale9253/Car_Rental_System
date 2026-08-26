from app.repositories.database import get_connection


class BrandRepository:

    def save(self, brand):
        connection = get_connection()
        cursor = connection.cursor()

        sql = """
        INSERT INTO brands (name)
        VALUES (%s)
        """

        values = (brand.name,)

        cursor.execute(sql, values)
        connection.commit()

        brand.id = cursor.lastrowid

        cursor.close()
        connection.close()

        return brand

    def find_by_id(self, brand_id):
        connection = get_connection()
        cursor = connection.cursor()

        sql = """
        SELECT id, name
        FROM brands
        WHERE id = %s
        """

        cursor.execute(sql, (brand_id,))

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result

    def find_all(self):
        connection = get_connection()
        cursor = connection.cursor()

        sql = """
        SELECT id, name
        FROM brands
        """

        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        return results

    def update(self, brand):
        connection = get_connection()
        cursor = connection.cursor()

        sql = """
        UPDATE brands
        SET name = %s
        WHERE id = %s
        """

        values = (
            brand.name,
            brand.id
        )

        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()

    def delete(self, brand_id):
        connection = get_connection()
        cursor = connection.cursor()

        sql = """
        DELETE FROM brands
        WHERE id = %s
        """

        cursor.execute(sql, (brand_id,))
        connection.commit()

        cursor.close()
        connection.close()