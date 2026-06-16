from database import engine
from sqlalchemy import text


def get_positions():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT position_name
            FROM positions
            ORDER BY position_name
            """)
        )

        rows = result.fetchall()

    return [r[0] for r in rows]


def add_position(position_name):

    with engine.connect() as conn:

        conn.execute(
            text("""
            INSERT INTO positions(
                position_name
            )
            VALUES(
                :position_name
            )
            """),
            {
                "position_name": position_name
            }
        )

        conn.commit()